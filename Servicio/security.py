from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Security, Cookie
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import ValidationError
from .schema.auth import *
from .settings import Settings
from .auth_repository import get_user
from .database import get_db

settings = Settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"employee": "Cambio de clave, vista de home"},
)


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUT = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def verify_password(plain_password, hashed_password):
    # Recibe la contraseña en texto plano y realiza la comparacion
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# Esta funcion verifica que exista un usuario con esas credenciales
# en caso True retorna el usuario
# En caso False retorna False
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(username, db=db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()  # Crea una copia de los datos de login
    # Verifica si existe tiempo de expiracion
    # Define la fecha y hora de expiracion con con expire_delta
    # o por defecto a 15 minutos
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # Agrega la eexpiraciona al objeto codificable
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # Codifica los elementos y los retorna
    return encoded_jwt


# Funcion que recupera el usuario actual
async def get_current_user(
    security_scopes: SecurityScopes,
    db: Annotated[AsyncSession, Depends(get_db)],
    access_token: str = Cookie(None),
):
    # Esta seccion prepara la respuesta http
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope= "{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            access_token, SECRET_KEY, algorithms=[ALGORITHM]
        )  # Decofica la carga util del JWT

        username: str = payload.get("sub")  # recupera el nombre de usuario
        if (
            username is None
        ):  # Si no hay nombre retorna la respuesta credentials_exception
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        print('Los scopes son',token_scopes)
        token_data = TokenData(
            scopes=token_scopes, username=username
        )  # valida y Crea el schema de datos
    except ExpiredSignatureError:  # Token ha expirado
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": authenticate_value},
        )
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    
    user = await get_user(
        user_name=token_data.username, db=db
    )  # Consulta si existe el suaurio en DB
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user  # Si hay lo retorna


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user)],
):
    # print(access_token)
    # print(current_user)
    # if current_user.disabled:  # Si el usuario no esta deshabilitado lo retona
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
