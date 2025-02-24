from fastapi import APIRouter, Depends, status, HTTPException, Security
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from ..security import get_current_active_user
from ..Utils.ifTable import interfaceTable
from ..function import iftables
from ..slim.slim_set import Set
from ..slim.slim_get import slim_get
from ..schema import aditional_schemas as schema
import asyncio


router = APIRouter(
    prefix="",
    tags=["ADDITIONALS"],
    dependencies=[Security(get_current_active_user, scopes=["administrator"])],
)


# Recupera la iftable del agente en cuestion  (View : Info)
@router.get("/iftable/{host}", response_model=list[schema.iftable])
async def read_agents(host: str):

    community = "public"
    iftableregister = iftables.get(host)
    if iftableregister:
        return iftableregister
    else:
        await asyncio.sleep(0.3)
        iftable = await interfaceTable(community, host)

        if iftable:
            iftables[host] = iftable

            return iftable
        else:
            raise HTTPException(status_code=400, detail="You cannot acquire the ifable")


@router.post(
    "/snmp/set/", dependencies=[Security(get_current_active_user, scopes=["snmp:set"])]
)
async def new_feature(operation: schema.operation):
    state = await Set("public", operation.ip, 161, operation.oid, operation.value)
    if not state:
        raise HTTPException(status_code=400, detail="ya existe o esta desconectado")


@router.post(
    "/snmp/get/", dependencies=[Security(get_current_active_user, scopes=["snmp:get"])]
)
async def new_feature(operation: schema.operation):
    print(operation)
    oid = ObjectType(ObjectIdentity(operation.oid))
    state = await slim_get("public", operation.ip, 161, oid)
    if state:
        _, value = state[0]
        return value
    else:
        raise HTTPException(status_code=400, detail="ya existe o esta desconectado")
