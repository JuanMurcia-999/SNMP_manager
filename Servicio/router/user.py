from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from ..security import get_current_active_user
from ..database import get_db
from ..schema.user import User, ChangePassword
from ..user_repository import (
    create_new_user,
    delete_user,
    get_one_user,
    get_one_user_scopes,
)
from ..services.user_service import password_change_service

router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Security(get_current_active_user, scopes=["administrator"])],
)


@router.get(
    "/search/one/{username}",
    dependencies=[Security(get_current_active_user, scopes=["user:read"])],
)
async def search_one_user(username: str, db: AsyncSession = Depends(get_db)):
    return await get_one_user(user_name=username, db=db)


@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED
    # dependencies=[Security(get_current_active_user, scopes=["user:create"])],
)
async def new_user(new_user: User, db: AsyncSession = Depends(get_db)):
    try:
        await create_new_user(new_user=new_user, db=db)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete(
    "/delete/{username}",
    status_code=status.HTTP_204_NO_CONTENT
    # dependencies=[Security(get_current_active_user, scopes=["user:delete"])],
)
async def delete_one_user(username: str, db: AsyncSession = Depends(get_db)):
    await delete_user(user_name=username, db=db)


@router.patch("/password/change", status_code=status.HTTP_202_ACCEPTED)
async def change_password(
    new_password: ChangePassword, db: AsyncSession = Depends(get_db)
):
    await password_change_service(new_password, db=db)


@router.get("/test/scopes/{id}")
async def get_scopes_user(id: str, db: AsyncSession = Depends(get_db)):
    return await get_one_user_scopes(user_name=id, db=db)
