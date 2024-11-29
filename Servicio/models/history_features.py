from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from ..database import Base



class History_features(Base):
    __tablename__ = "history_features"

    id_register = Column(Integer, autoincrement=True, primary_key=True)
    id_agent = Column(Integer, ForeignKey("agents.id_agent"), nullable=False)
    id_adminis = Column(
        Integer, ForeignKey("administered_features.id_adminis"), nullable=False
    )
    value = Column(Float, nullable=False)

    date = Column(String(100))
    time = Column(String(100))

    agent = relationship("Agents", back_populates="history")
    feature = relationship("Administered_features")
