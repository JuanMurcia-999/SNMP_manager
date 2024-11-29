from fastapi import APIRouter, Depends, status, HTTPException, Security, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schema import agents_schemas as schema
from ..services import agents_services as crud
from ..models.agent import ModelField
from ..function import create_instance_from_Manageable, instances
from ..Utils.Gestionables import Ping
from ..security import get_current_active_user


router = APIRouter(
    prefix="/agents",
    tags=["AGENTS"],
    dependencies=[Security(get_current_active_user, scopes=["administrator"])],
)


# recuepra la informacion de todos los agentes
@router.get(
    "/all/", dependencies=[Security(get_current_active_user, scopes=["agent:read"])]
)
async def read_agents(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_agent(db=db)


# Agregar agente
@router.post(
    "/create/",
    dependencies=[Security(get_current_active_user, scopes=["agent:create"])],
    status_code=status.HTTP_201_CREATED,
)
async def create_agent(agent: schema.CreateAgent, db: AsyncSession = Depends(get_db)):
    id_agent = await crud.create_agent(db=db, agent=agent)
    if id_agent:
        data = {
            "ag_name": agent.ag_name,
            "ip_address": agent.ip_address,
            "ag_type": agent.ag_type,
            "id_agent": id_agent,
        }
        Agent = schema.Agent(**data)
        instance = await create_instance_from_Manageable(Agent)
        instances[agent.ag_name] = instance
        await instance.task_oid()

    else:
        raise HTTPException(status_code=400, detail="ya agregado o error")


# elimina agentes
@router.delete(
    "/delete/{field}",
    dependencies=[Security(get_current_active_user, scopes=["agent:delete"])],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_agent(field: ModelField, value, db: AsyncSession = Depends(get_db)):
    db_agent = await crud.delete_agent(db=db, field=field.name, value=value)
    if db_agent:
        instance = instances.get(db_agent.ag_name)
        await instance.cancel_end()
        del instances[db_agent.ag_name]
        await Ping().deleteagent(db_agent.id_agent)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El agente no existe"
        )
