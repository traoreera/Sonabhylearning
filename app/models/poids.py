from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker
from .database import Base



class Poids(Base):
    __tablename__ = 'poids'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    real_weight = Column(Float)
    measured_weight = Column(Float)
    tolerance = Column(Float, default=0.02)
    
    def responseModels(self):
        return {
            "date": self.date,
            "real_weight": self.real_weight,
            "measured_weight": self.measured_weight,
            "tolerance": self.tolerance
        }