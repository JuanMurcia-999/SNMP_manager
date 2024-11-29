from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base



class Administered_features(Base):
    __tablename__ = "administered_features"

    id_adminis = Column(Integer, autoincrement=True, primary_key=True)
    id_sensor = Column(Integer, nullable=True)
    id_agent = Column(Integer, ForeignKey("agents.id_agent"), nullable=False)
    oid = Column(String(100), nullable=False)
    adminis_name = Column(String(100), nullable=False)
    timer = Column(Integer, nullable=False)

    agent = relationship("Agents", back_populates="features")
    alarms = relationship(
        "Alarms",
        back_populates="administered_feature",
        cascade="all, delete, delete-orphan",
    )
