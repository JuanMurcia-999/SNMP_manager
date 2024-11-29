from ..database import get_db
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from ..models.active_default import Active_default


async def get_sensors_startup(id):
    async for db in get_db():
        try:
            return (
                (
                    await db.execute(
                        select(Active_default)
                        .options(joinedload(Active_default.features))
                        .filter(Active_default.id_agent == id)
                    )
                )
                .scalars()
                .all()
            )

        except Exception:
            print("fallo en get_sensors_startup")