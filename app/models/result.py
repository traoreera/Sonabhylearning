from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from app.models.database import Base



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
