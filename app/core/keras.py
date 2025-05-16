import os
import numpy as np
import tensorflow as tf
from datetime import timedelta
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from app.models.database import get_db
from sklearn.metrics import mean_absolute_error, mean_squared_error
from app.models.poids import Poids

session = next(get_db())


class KerasLLM:
    def __init__(self):
        self.model_name = "Linear Regression Model"
        self.model_type = "Regression"
        self.model_path = "./LLMmodels/keras_llm.keras"
        
        
        self.records = session.query(Poids).order_by(Poids.date).all()
        self.base_date = self.records[0].date.date()

        if os.path.exists(self.model_path):
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            self.train_model()

    def train_model(self):
        x = np.array([(r.date.date() - self.base_date).days for r in self.records]).reshape(-1, 1)
        y = np.array([abs(r.real_weight - r.measured_weight) * 1000 for r in self.records])  # erreur en grammes

        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(x.shape[1],)),
            Dense(64, activation='relu'),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')
        self.model.fit(x, y, epochs=100, batch_size=32, verbose=0)
        self.save()

    def predict_date_tolerance_exceeded(self, poids_actuel, poids_attendu, tolerance, date_mesure, jours_max=30):
        current_error = abs(poids_actuel - poids_attendu) * 1000  # erreur en grammes

        for i in range(jours_max):
            future_date = date_mesure + timedelta(days=i)
            days_since_base = (future_date.date() - self.base_date).days
            X_input = np.array([[days_since_base]])
            predicted_error = self.model.predict(X_input, verbose=0)[0][0]

            if predicted_error > tolerance:
                return future_date, predicted_error, current_error
        self.save()
        return None, None, current_error

    def evaluate(self):
        """
        Évalue les performances du modèle avec MAE et RMSE.
        """
        x = np.array([(r.date.date() - self.base_date).days for r in self.records]).reshape(-1, 1)
        y_true = np.array([abs(r.real_weight - r.measured_weight) * 1000 for r in self.records])
        y_pred = self.model.predict(x, verbose=0)

        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return {"MAE": mae, "RMSE": rmse}

    def save(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)




class KerasMultiFeatureLLM:
    def __init__(self):
        self.model_path = "./LLMmodels/keras_multi_llm.keras"
        self.records = session.query(Poids).order_by(Poids.date).all()
        self.base_date = self.records[0].date.date()

        if os.path.exists(self.model_path):
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            self.train_model()

    def train_model(self):
        X, y = self.prepare_data()

        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(3,)),
            Dense(64, activation='relu'),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')
        self.model.fit(X, y, epochs=100, batch_size=32, verbose=0)
        self.save()

    def prepare_data(self):
        X = []
        y = []

        for r in self.records:
            days_since_base = (r.date.date() - self.base_date).days
            poids_attendu = r.real_weight
            poids_mesure = r.measured_weight
            erreur = abs(poids_attendu - poids_mesure) * 1000  # en grammes

            X.append([days_since_base, poids_attendu, poids_mesure])
            y.append(erreur)

        return np.array(X), np.array(y)

    def predict(self, days_since_base, poids_attendu, poids_mesure):
        X_input = np.array([[days_since_base, poids_attendu, poids_mesure]])
        return self.model.predict(X_input, verbose=0)[0][0]

    def predict_date_tolerance_exceeded(self, poids_attendu, poids_mesure, tolerance, date_mesure, jours_max=30):
        for i in range(jours_max):
            future_date = date_mesure + timedelta(days=i)
            days_since_base = (future_date.date() - self.base_date).days
            predicted_error = self.predict(days_since_base, poids_attendu, poids_mesure)

            if predicted_error > tolerance:
                return future_date, predicted_error
        self.save()
        return None, None

    def evaluate(self):
        X, y_true = self.prepare_data()
        y_pred = self.model.predict(X, verbose=0)

        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))

        return {"MAE": mae, "RMSE": rmse}

    def save(self):
        os.makedirs('./LLMmodels', exist_ok=True)
        self.model.save(self.model_path)
        


class mainTest:
    def __init__(self):
        self.model_path = "./llmodels/keras_multi_llm.keras"
        self.records = session.query(Poids).order_by(Poids.date).all()
        self.base_date = self.records[0].date.date()

        if os.path.exists(self.model_path):
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            self.train_model()

    def train_model(self):
        X = []
        y = []

        for r in self.records:
            days_since_base = (r.date.date() - self.base_date).days
            poids_attendu = r.real_weight
            poids_mesure = r.measured_weight
            erreur = abs(poids_attendu - poids_mesure) * 1000  # en g

            X.append([days_since_base, poids_attendu, poids_mesure])
            y.append(erreur)

        X = np.array(X)
        y = np.array(y)

        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(3,)),
            Dense(64, activation='relu'),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')
        self.model.fit(X, y, epochs=100, batch_size=32, verbose=0)
        self.save()

    def predict(self, days_since_base, poids_attendu, poids_mesure):
        X_input = np.array([[days_since_base, poids_attendu, poids_mesure]])
        return self.model.predict(X_input, verbose=0)[0][0]

    def predict_date_tolerance_exceeded(self, poids_attendu, poids_mesure, tolerance, date_mesure, jours_max=30):
        for i in range(jours_max):
            future_date = date_mesure + timedelta(days=i)
            days_since_base = (future_date.date() - self.base_date).days
            predicted_error = self.predict(days_since_base, poids_attendu, poids_mesure)

            if predicted_error > tolerance:
                return future_date, predicted_error

        return None, None

    def save(self):
        os.makedirs('./llmodels', exist_ok=True)
        self.model.save(self.model_path)