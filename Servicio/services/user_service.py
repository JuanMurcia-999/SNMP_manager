from sqlalchemy.ext.asyncio import AsyncSession
from ..schema.user import ChangePassword
from ..auth_repository import get_user, update_password
from ..security import verify_password, get_password_hash
from fastapi import HTTPException, status


async def password_change_service(new_password: ChangePassword, db: AsyncSession):

    if new_password.new_password != new_password.repeat_password:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Passwords do not match"
        )
    user = await get_user(user_name=new_password.username, db=db)
    if not verify_password(new_password.previous_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password incorrect"
        )
    new = get_password_hash(new_password.new_password)
    await update_password(new_password.username, new, db=db)
