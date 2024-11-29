from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .models.users import Users
from .schema.user import User


async def get_user(user_name: str, db: AsyncSession):
    status_faile = HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="El usuario no existe",
    )

    try:
    
        result = await db.execute(select(Users).filter(Users.username == user_name))
        user = result.scalars().first()
        user_dict = {key: value for key, value in user.__dict__.items() if not key.startswith('_')}
        return User(**user_dict)
    except Exception as e:
        raise status_faile



async def update_password(user_name:str , new_password,db:AsyncSession):
    status_faile = HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="No es posible actualizar",
    )

    try:
        await db.execute(update(Users).filter(Users.username == user_name).values(password=new_password))
        await db.commit()
    except Exception as e:
        print(e)
        raise status_faile