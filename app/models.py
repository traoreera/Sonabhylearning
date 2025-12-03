from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database import Base



# --- Création des modèles ---
class ResulttLineareRegretion(Base):
    __tablename__ = 'resultatsLR'
    id = Column(Integer, primary_key=True)
    predicted_date = Column(String)
    predicted_error = Column(Float)
    tolerance = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    

class RGDResult(Base):
    __tablename__ = 'resultatsRGD'
    id = Column(Integer, primary_key=True)
    predicted_date = Column(String)
    predicted_error = Column(Float)
    tolerance = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class KerasResultSimple(Base):
    __tablename__ = 'resultatsKerasSimple'
    id = Column(Integer, primary_key=True)
    predicted_date = Column(String)
    predicted_error = Column(Float)
    tolerance = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class KerasResultMulti(Base):
    __tablename__ = 'resultatsKerasMulti'
    id = Column(Integer, primary_key=True)
    predicted_date = Column(String)
    predicted_error = Column(Float)
    tolerance = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Poids(Base):
    __tablename__ = 'poids'
    id = Column(Integer, primary_key=True, autoincrement=True)
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