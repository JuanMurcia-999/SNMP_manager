from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base



class Types(Base):
    __tablename__ = "types"

    id_type = Column(Integer, autoincrement=True, primary_key=True)
    type_name = Column(String(30), nullable=False, unique=True)

    agents = relationship("Agents", back_populates="type")
    defaultfeatures = relationship("Default_features", back_populates="type")
