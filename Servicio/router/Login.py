from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from datetime import timedelta

from ..settings import settings
from ..security import authenticate_user, create_access_token
from ..database import get_db
from ..schema.auth import *
from ..user_repository import get_scopes




router= APIRouter(tags=['Login'])


@router.post("/token")
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],  # Recupera los elementos del formulario recibido
    db: AsyncSession= Depends(get_db)
):
    
    user = await authenticate_user(db, form_data.username, form_data.password) #Recupera el usuario

    if not user:   # Si no existe el usuario lanza la advertencia
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #Si existe 
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)) #Formatea el tiempo de expiracion
    #Crea el access token con la informacion del usuario y los scopes
    scopes_string = await get_scopes(user=user, db=db)
    scopes= scopes_string.split()  
    print(scopes)

    access_token = create_access_token( 
        data={"sub": user.username, "scopes": scopes}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  
        secure=True,    
        samesite="None",  
        max_age=1800,   
    )

    return scopes

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="Lax"
    )
    return JSONResponse(content={"message": "Cierre de sesión exitoso"}, status_code=status.HTTP_200_OK)