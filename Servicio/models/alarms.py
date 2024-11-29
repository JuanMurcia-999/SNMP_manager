from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


class Alarms(Base):
    __tablename__ = "alarms"

    id_alarm = Column(Integer, autoincrement=True, primary_key=True)
    id_agent = Column(Integer, ForeignKey("agents.id_agent"), nullable=False)
    id_adminis = Column(
        Integer, ForeignKey("administered_features.id_adminis"), nullable=True
    )
    id_sensor = Column(Integer, nullable=True)
    operation = Column(String(50), nullable=False)
    value = Column(Integer, nullable=False)
    counter = Column(Integer, nullable=True)

    administered_feature = relationship(
        "Administered_features", back_populates="alarms"
    )
