from ..database import get_db
from sqlalchemy.future import select
from sqlalchemy import and_
from ..models.history_features import History_features
from ..models.administered_features import Administered_features
from ..models.alarms import Alarms


async def add_history(data):
    async for db in get_db():
        try:
            async for db in get_db():
                db_history = History_features(
                    id_agent=data.id_agent,
                    id_adminis=data.id_adminis,
                    value=data.value,
                    time=data.Time,
                    date=data.Date,
                )

                db.add(db_history)
                await db.commit()
                await db.refresh(db_history)
                return True
        except Exception:
            print("algo paso add_history")
            return False


async def get_administered_feature(column: str, tarea):
    async for db in get_db():
        try:
            query = await db.execute(
                select(Administered_features).filter(
                    getattr(Administered_features, column) == tarea.id_adminis
                )
            )
            return query.scalars().first()
        except Exception:
            print("fallo en get_administered_feature")


async def get_alarms(column: str, data):
    async for db in get_db():
        try:
            result = await db.execute(
                select(Alarms)
                .join(
                    Administered_features,
                    Alarms.id_adminis == Administered_features.id_adminis,
                )
                .filter(
                    and_(
                        getattr(Administered_features, column)
                        == data.id_adminis,
                        Administered_features.id_agent == data.id_agent,
                    )
                )
            )

            return result.scalars().all()
        except Exception:
            print("fallo en get_alarms")
