from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


class Default_features(Base):
    __tablename__ = "default_features"

    id_feature = Column(Integer, autoincrement=True, primary_key=True)
    fe_name = Column(String(100), nullable=False)
    id_type = Column(Integer, ForeignKey("types.id_type"), nullable=False)

    type = relationship("Types", back_populates="defaultfeatures")
