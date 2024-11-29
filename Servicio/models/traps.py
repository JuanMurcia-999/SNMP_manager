from sqlalchemy import Column, Integer, String, Date, Time, Text

from ..database import Base
from sqlalchemy.sql import func


class Traps(Base):
    __tablename__ = "traps"

    id_alarm = Column(Integer, autoincrement=True, primary_key=True)
    ip = Column(String(100), nullable=False)
    message = Column(Text, nullable=True)
    date = Column(Date, server_default=func.current_date())
    time = Column(Time, server_default=func.current_time())
