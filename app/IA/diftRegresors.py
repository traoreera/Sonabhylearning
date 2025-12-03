import os
import json
import joblib
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from app.database import get_db
from app.models import Poids

class DriftRegressor:
    """
    Régression linéaire pour prédire quand la dérive du poids mesuré dépasse une tolérance.
    Tout en kg, normalisation automatique des jours.
    Supporte LinearRegression et SGDRegressor.
    model_type : "linear" ou "sgd"
    tolerance : tolérance en kg
    model_dir : dossier de sauvegarde
    
    """

    def __init__(self, model_type="linear", tolerance=0.2, model_dir="./LLMmodels"):
        self.model_type = model_type.lower()
        self.tolerance = tolerance  # kg
        self.model_dir = model_dir
        self.model_path = os.path.join(model_dir, f"{self.model_type}_regressor.pkl")
        self.meta_path = os.path.join(model_dir, f"{self.model_type}_info.json")
        os.makedirs(self.model_dir, exist_ok=True)

        # Session DB
        self.session = next(get_db())
        self.dates, self.errors = self._load_data()
        self.base_date = self.dates[0] if self.dates else None
        self.days = self._normalize_days(self.dates, self.base_date) if self.dates else None

        # Model
        self.model = self._load_or_create_model()

    # ---------------------------
    #  DATA HANDLING
    # ---------------------------
    def _load_data(self):
        try:
            records = self.session.query(Poids).order_by(Poids.date).all()
            if len(records) < 2:
                return None, None
            dates = [r.date for r in records]
            errors = [abs(r.measured_weight - r.real_weight) for r in records]  # kg
            return dates, np.array(errors, dtype=np.float64)
        except Exception as e:
            print(f"Error loading data: {e}")
            return None, None

    def refresh_data(self):
        self.dates, self.errors = self._load_data()
        self.base_date = self.dates[0] if self.dates else None
        self.days = self._normalize_days(self.dates, self.base_date) if self.dates else None

    def _normalize_days(self, dates, base_date):
        """Normalisation pour éviter explosions numériques (SGD sensible aux grands nombres)"""
        return np.array([(d - base_date).days for d in dates], dtype=np.float64).reshape(-1, 1) / 100.0

    # ---------------------------
    #  MODEL MANAGEMENT
    # ---------------------------
    def _load_or_create_model(self):
        if os.path.exists(self.model_path):
            try:
                model = joblib.load(self.model_path)
                print(f"✅ Model loaded from {self.model_path}")
                return model
            except Exception:
                print("⚠️ Failed to load model, creating a new one.")
        return self._create_model()

    def _create_model(self):
        if self.model_type == "sgd":
            return SGDRegressor(max_iter=1000, tol=1e-3, penalty="l2", random_state=42,
                                learning_rate='adaptive', eta0=0.01)
        elif self.model_type == "linear":
            return LinearRegression()
        else:
            raise ValueError("model_type must be 'linear' or 'sgd'")

    # ---------------------------
    #  TRAINING
    # ---------------------------
    def train(self, incremental=False):
        if self.dates is None or len(self.errors) < 2:
            print("⚠️ Not enough data for training")
            return None
        if incremental and self.model_type == "sgd" and os.path.exists(self.model_path):
            self.model.partial_fit(self.days, self.errors)
        else:
            self.model.fit(self.days, self.errors)
        metrics = self.evaluate()
        self._save(metrics)
        return metrics

    def train_from_series(self, dates, expected_values, measured_values, incremental=False):
        if not (len(dates) == len(expected_values) == len(measured_values)):
            raise ValueError("All input lists must have the same length.")
        self.dates = dates
        self.errors = np.array([abs(m - e) for e, m in zip(expected_values, measured_values)], dtype=np.float64)
        self.base_date = self.dates[0]
        self.days = self._normalize_days(self.dates, self.base_date)
        return self.train(incremental=incremental)

    # ---------------------------
    #  PREDICTION
    # ---------------------------
    def predict_error_at_date(self, target_date):
        if self.base_date is None:
            return None
        days = (target_date - self.base_date).days / 100.0
        pred = self.model.predict([[days]])[0]
        return max(0, float(pred))  # kg

    def predict_tolerance_breach(self):
        if self.days is None or len(self.errors) < 2:
            return None, None
        coef = float(self.model.coef_[0])
        intercept = float(self.model.intercept_ if isinstance(self.model.intercept_, float) else self.model.intercept_[0])
        current_error = float(self.errors[-1])
        if coef <= 1e-6:
            return None, current_error
        predicted_day = (self.tolerance - intercept) / coef
        if predicted_day <= self.days[-1][0]:
            return datetime.now(), current_error
        predicted_date = self.base_date + timedelta(days=int(predicted_day*100))  # dénormalisation
        return predicted_date, current_error

    # ---------------------------
    #  EVALUATION
    # ---------------------------
    def evaluate(self):
        # Pas assez de données -> inutile d'évaluer
        if self.days is None or len(self.errors) < 2:
            return None

        # Vérifier si le modèle est entraîné
        if not hasattr(self.model, "coef_"):
            # auto-fit pour éviter l'erreur
            self.model.fit(self.days, self.errors)

        predictions = self.model.predict(self.days)

        mae = mean_absolute_error(self.errors, predictions)
        rmse = np.sqrt(mean_squared_error(self.errors, predictions))
        r2 = r2_score(self.errors, predictions)

        return {
            "MAE": float(mae),
            "RMSE": float(rmse),
            "R2": float(r2),
            "drift_rate_kg_per_day": float(self.model.coef_[0])
        }


    # ---------------------------
    #  SAVE
    # ---------------------------
    def _save(self, metrics=None):
        joblib.dump(self.model, self.model_path)
        metadata = {
            "model_type": self.model_type,
            "tolerance_kg": self.tolerance,
            "dataset_size": len(self.errors) if self.errors is not None else 0,
            "last_update": datetime.now().isoformat(),
            "base_date": self.base_date.isoformat() if self.base_date else None,
            "metrics": metrics
        }
        with open(self.meta_path, "w") as f:
            json.dump(metadata, f, indent=2)
        print(f"💾 Model saved to {self.model_path}")



    def predict_weight_error(self, date, poids_attendu=None, poids_mesure=None):
        """
        Prédit l’erreur future à une date donnée.
        Comme le modèle est basé uniquement sur le temps, les poids ne sont pas utilisés.
        """
        if self.base_date is None:
            raise RuntimeError("Model not trained — no base date found.")

        # Normalisation identique à l'entraînement
        days_normalized = ((date - self.base_date).days) / 100.0

        prediction = float(self.model.predict([[days_normalized]])[0])
        return max(0, prediction)  # pas d'erreur négative




    def predict(self, date, mesure, attendu=None):
        """
        Prédit l'erreur future et calcule l'erreur actuelle si les valeurs sont fournies.
        - date: datetime
        - mesure: poids mesuré à cette date (kg)
        - attendu: poids attendu (kg) -> optionnel
        
        Retourne dict:
        {
            "timestamp": date,
            "current_error": erreur calculée (si attendu fourni),
            "predicted_error": erreur prédite par modèle,
            "tolerance_breach": True/False
        }
        """
        if self.base_date is None:
            raise RuntimeError("Model not trained — No base date.")

        # Normalisation identique à l'entraînement
        days_normalized = ((date - self.base_date).days) / 100.0
        predicted_error = float(self.model.predict([[days_normalized]])[0])
        predicted_error = max(0, predicted_error)

        current_error = None
        if attendu is not None:
            current_error = abs(mesure - attendu)

        breach = predicted_error >= self.tolerance

        return {
            "timestamp": date,
            "current_error": current_error,
            "predicted_error": predicted_error,
            "tolerance_breach": breach
        }

    def get_date_tolerance_breach(self):
        if self.days is None or len(self.errors) < 2:
            return None
        coef = float(self.model.coef_[0])
        intercept = float(self.model.intercept_ if isinstance(self.model.intercept_, float) else self.model.intercept_[0])
        if coef <= 1e-6:
            return None
        predicted_day = (self.tolerance - intercept) / coef
        if predicted_day <= self.days[-1][0]:
            return None
        predicted_date = self.base_date + timedelta(days=int(predicted_day*100))  # dénormalisation
        return predicted_date