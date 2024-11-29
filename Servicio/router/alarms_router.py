from fastapi import APIRouter, Depends, status, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schema import alarms_schemas as schema
from ..services import alarms_services as crud
from ..security import get_current_active_user


router = APIRouter(
    prefix="/alarms",
    tags=["ALARMS"],
    dependencies=[Security(get_current_active_user, scopes=["administrator"])],
)


# Eliminar alarmas
@router.get(
    "/all/",
    dependencies=[Security(get_current_active_user, scopes=["alarm:read"])],
    response_model=list[schema.readAlarm],
)
async def read_agents(id_agent: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_alarm(db=db, id_agent=id_agent)


# Eliminar las alarmas
@router.delete(
    "/delete/",
    dependencies=[Security(get_current_active_user, scopes=["alarm:delete"])],
)
async def delete_feature(id: int, db: AsyncSession = Depends(get_db)):
    state = await crud.delete_alarm(db=db, id_alarm=id)
    if state:
        raise HTTPException(status_code=200, detail="Alarma Eliminada")
    else:
        raise HTTPException(status_code=400, detail="Alarma ya eliminada")


# Crear alarmas
@router.post(
    "/new/", dependencies=[Security(get_current_active_user, scopes=["alarm:create"])]
)
async def new_alarm(alarm: schema.newAlarm, db: AsyncSession = Depends(get_db)):
    state = await crud.add_alarm(db=db, alarm=alarm)
    if state:
        raise HTTPException(status_code=200, detail="Alarma agregada")
