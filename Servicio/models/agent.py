from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base
from enum import Enum
from .types import Types


class ModelField(str, Enum):
    id_agent = "ID"
    ag_name = "name"
    ip_address = "IP"


class Agents(Base):
    __tablename__ = "agents"

    id_agent = Column(Integer, autoincrement=True, primary_key=True)
    ag_name = Column(String(50), nullable=False, unique=True)
    ip_address = Column(String(50), nullable=False, unique=True)
    ag_type = Column(Integer, ForeignKey("types.id_type"), nullable=False)

    type = relationship("Types", back_populates="agents")
    features = relationship(    
        "Administered_features", cascade="all, delete", back_populates="agent"
    )
    history = relationship(
        "History_features", cascade="all, delete", back_populates="agent"
    )
    Alarms = relationship("Alarms", cascade="all, delete")
    Actives = relationship(
        "Active_default", cascade="all,delete", back_populates="agents"
    )
