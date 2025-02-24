from fastapi import APIRouter, Depends, status, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schema import history_schemas as schema
from ..services import history_services as crud
from ..abstractions import Abstractions
from ..security import get_current_active_user

router = APIRouter(
    prefix="/history",
    tags=["HISTORY"],
    dependencies=[Security(get_current_active_user, scopes=["administrator"])],
)


# Obtener el historial segun el sensor (OID)
@router.post(
    "/sensor/",
    dependencies=[Security(get_current_active_user, scopes=["history:sensor"])],
)
async def read_history_sensor(
    filter: schema.getHistory, db: AsyncSession = Depends(get_db)
):
    if filter.id_sensor == 100:
        return await crud.get_history_Network(db=db, filter=filter)
    else:
        return await crud.get_history_sensor(db=db, filter=filter)


@router.post(
    "/filter/",
    dependencies=[Security(get_current_active_user, scopes=["history:filter"])],
)
async def read_history_sensor(
    filter: schema.filterHistory, db: AsyncSession = Depends(get_db)
):
    if filter.id_sensor == 105:
        dato = f"{filter.id_sensor}{filter.id_agent}"
        return await Abstractions().CPU(dato, filter)
    elif str(filter.id_sensor).startswith("100"):
        return await Abstractions().NETWORK(filter)
    else:
        return await crud.get_history_filter(db=db, filter=filter)
