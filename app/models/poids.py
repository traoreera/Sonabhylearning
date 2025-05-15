from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker
from .database import Base



class Poids(Base):
    __tablename__ = 'poids'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    real_weight = Column(Float)
    measured_weight = Column(Float)
    tolerance = Column(Float, default=2.0)