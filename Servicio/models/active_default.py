from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from ..database import Base



class Active_default(Base):
    __tablename__ = "active_default"

    id_active = Column(Integer, autoincrement=True)
    id_feature = Column(
        Integer,
        ForeignKey("default_features.id_feature"),
        nullable=False,
        primary_key=True,
    )
    id_agent = Column(
        Integer, ForeignKey("agents.id_agent"), nullable=False, primary_key=True
    )
    params = Column(Text, nullable=True)

    features = relationship("Default_features")
    agents = relationship("Agents", back_populates="Actives")
