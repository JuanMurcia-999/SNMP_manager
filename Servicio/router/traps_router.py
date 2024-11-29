from fastapi import APIRouter, Depends, status, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import traps_services as crud
from ..database import get_db
from ..security import get_current_active_user

router = APIRouter(
    prefix="/traps",
    tags=["TRAPS"],
    dependencies=[Security(get_current_active_user, scopes=["administrator"])],
)


@router.get(
    "/all/",
    dependencies=[Security(get_current_active_user, scopes=["traps:read:all"])],
)
async def get_traps(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_traps(db=db)


@router.get(
    "/message/{ID}",
    dependencies=[Security(get_current_active_user, scopes=["traps:read:detail"])],
)
async def get_trap_message(ID, db: AsyncSession = Depends(get_db)):
    return await crud.get_trap_message(db=db, value=ID)
