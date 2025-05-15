from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sklearn.linear_model import LinearRegression, SGDRegressor
# --- Configuration de la base de données ---
Base = declarative_base()


def get_db():
    engine = create_engine('sqlite:///base_de_donnees.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session