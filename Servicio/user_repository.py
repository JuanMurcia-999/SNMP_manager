from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from .models.permission import Permissions
from .models.users import Users
from .security import get_password_hash
from .schema.user import User


async def get_one_user(user_name: str, db: AsyncSession):
    status_file = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="No exist user"
    )
    try:
        result = await db.execute(select(Users).filter(Users.username == user_name))
        return result.scalars().first()
    except Exception:
        raise status_file


async def create_new_user(new_user: User, db: AsyncSession):
    status_file = HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe"
    )

    try:
        result = await db.execute(
            select(Users).filter(Users.username == new_user.username)
        )
        duplicate = result.scalars().first()
        if duplicate:
            raise status_file
        db_user = Users(
            username=new_user.username,
            password=get_password_hash(new_user.password),
            role_id=new_user.role_id,
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    except Exception as e:
        print(e)
        raise status_file


async def delete_user(user_name: str, db: AsyncSession):
    status_faile = HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="El usuario no existe",
    )

    try:
        result = await db.execute(select(Users).filter(Users.username == user_name))
        db_employee = result.scalars().first()
        if db_employee:
            await db.delete(db_employee)
            await db.commit()
        else:
            raise status_faile
    except Exception:
        raise status_faile


async def get_scopes(user: Users, db: AsyncSession):

    status_file = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="No possible GET"
    )
    try:
        resultOne = await db.execute(
            select(Permissions.permission_name).filter(
                Permissions.role_id == user.role_id
            )
        )

        permission_role = resultOne.scalars().first()

        return permission_role
    except Exception:
        raise status_file


async def get_one_user_scopes(user_name: str, db: AsyncSession):
    status_file = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="No exist user"
    )
    try:
        result = await db.execute(
            select(Users)
            .filter(Users.username == user_name)
            .options(selectinload(Users.scopes))
        )
        return result.scalars().all()
    except Exception as e:
        print()
        raise status_file
