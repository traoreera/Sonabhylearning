import os
import numpy as np
import joblib
from app.models.database import get_db
from app.models.poids import Poids
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression, SGDRegressor

session = next(get_db())

os.makedirs(name='./LLMmodels',exist_ok=True)

def SGDRegretions(tolerance):
    records = session.query(Poids).order_by(Poids.date).all()
    dates = [p.date for p in records]
    jours = np.array([(d - dates[0]).days for d in dates]).reshape(-1, 1)
    erreurs = np.array([abs(p.measured_weight - p.real_weight) * 1000 for p in records])  # en grammes    
    if os.path.exists('./LLMmodels/sgdRegretion.pkl'):
        print('file exist loading ... ')
        model = joblib.load('./LLMmodels/sgdRegretion.pkl')
        model.partial_fit(jours, erreurs)
        joblib.dump(model, './LLMmodels/sgdRegretion.pkl')
    else:
        print('file not exist creating ... ')
        model = SGDRegressor(max_iter=1000, tol=1e-3, penalty='l2', random_state=42)
        model.fit(jours,erreurs)
        joblib.dump(model, './LLMmodels/sgdRegretion.pkl')

    
    if len(records) < 2:
        return None, None


    

    coef = model.coef_[0]
    intercept = model.intercept_[0]

    if coef <= 0:
        return dates[-1], erreurs[-1]  # pas de dérive ascendante détectée

    jours_tolerance = (tolerance - intercept) / coef

    if jours_tolerance < 0:
        return datetime.now(), erreurs[-1]

    predicted_date = dates[0] + timedelta(days=int(jours_tolerance))
    predicted_error = model.predict([[jours[-1][0]]])[0]
    joblib.dump(model, './LLMmodels/sgdRegretion.pkl')
    return predicted_date, predicted_error

def LineareRegretion(tolerance):
    if os.path.exists('./LLMmodels/LineareRegretion.pkl'):
        model = joblib.load('./LLMmodels/LineareRegretion.pkl')
    records = session.query(Poids).order_by(Poids.date).all()
    if len(records) < 2:
        return None, None
    else:
        model = LinearRegression()
    dates = [p.date for p in records]
    jours = np.array([(d - dates[0]).days for d in dates]).reshape(-1, 1)
    erreurs = np.array([abs(p.measured_weight - p.real_weight) * 1000 for p in records])  # en grammes

    
    model.fit(jours, erreurs)

    if model.coef_[0] <= 0:
        return dates[-1], erreurs[-1]  # pas de dérive détectée

    jours_tolerance = (tolerance - model.intercept_) / model.coef_[0]

    if jours_tolerance < 0:
        return datetime.now(), erreurs[-1]

    predicted_date = dates[0] + timedelta(days=int(jours_tolerance))
    predicted_error = model.predict([[jours[-1][0]]])[0]
    joblib.dump(model,'./LLMmodels/LineareRegretion.pkl')
    return predicted_date, predicted_error


def RetraineLR():
    
    if os.path.exists('./LLMmodels/LineareRegretion.pkl'):
        model = joblib.load('./LLMmodels/LineareRegretion.pkl')
    records = session.query(Poids).order_by(Poids.date).all()
    
    if len(records) < 2:
        return None, None
    else:
        model = LinearRegression()
    
    dates = [p.date for p in records]
    jours = np.array([(d - dates[0]).days for d in dates]).reshape(-1, 1)
    erreurs = np.array([abs(p.measured_weight - p.real_weight) * 1000 for p in records])  # en grammes

    
    model.fit(jours, erreurs)
    
    os.makedirs('./LLMmodels', exist_ok=True)
    joblib.dump(model,'./LLMmodels/LineareRegretion.pkl')
    return


def RetraineSGD():
    
    records = session.query(Poids).order_by(Poids.date).all()
    dates = [p.date for p in records]
    jours = np.array([(d - dates[0]).days for d in dates]).reshape(-1, 1)
    erreurs = np.array([abs(p.measured_weight - p.real_weight) * 1000 for p in records])  # en grammes    
    if os.path.exists('./LLMmodels/sgdRegretion.pkl'):
        print('file exist loading ... ')
        model = joblib.load('./LLMmodels/sgdRegretion.pkl')
        model.partial_fit(jours, erreurs)
        joblib.dump(model, './LLMmodels/sgdRegretion.pkl')
    else:
        print('file not exist creating ... ')
        model = SGDRegressor(max_iter=1000, tol=1e-3, penalty='l2', random_state=42)
        model.fit(jours,erreurs)
        joblib.dump(model, './LLMmodels/sgdRegretion.pkl')
    
    model.fit(jours, erreurs)
    os.makedirs('./LLMmodels', exist_ok=True)
    joblib.dump(model,'./LLMmodels/sgdRegretion.pkl')
    return