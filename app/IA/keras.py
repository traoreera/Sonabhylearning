import os
import json
import numpy as np
import tensorflow as tf
from datetime import datetime, timedelta
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from app.database import get_db
from app.models import Poids


class WeightErrorRegressor:
    def __init__(self, 
                model_path="./models/weight_error.keras",
                metadata_path="./models/model_info.json",
                scaler_path="./models/scaler.pkl",
                version="1.0.0",
                seed=42):
        
        self.model_path = model_path
        self.metadata_path = metadata_path
        self.scaler_path = scaler_path
        self.version = version
        self.seed = seed
        
        # Set seeds for reproducibility
        tf.random.set_seed(seed)
        np.random.seed(seed)
        
        # Load data
        session = next(get_db())
        try:
            self.records = session.query(Poids).order_by(Poids.date).all()
            if not self.records:
                raise ValueError("No weight records found in database")
        finally:
            session.close()
        
        self.base_date = self.records[0].date.date()
        
        # Prepare data
        X, y = self._prepare_data()
        y = y.reshape(-1, 1)
        
        # Load or fit scaler
        if os.path.exists(self.scaler_path):
            import pickle
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            self.X_scaled = self.scaler.transform(X)
        else:
            self.scaler = StandardScaler()
            self.X_scaled = self.scaler.fit_transform(X)
            self._save_scaler()
        
        # Load or train model
        if os.path.exists(self.model_path):
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            self._train(self.X_scaled, y)
        
        self._update_metadata()
    
    def _prepare_data(self):
        """Prepare features and target from database records"""
        X, y = [], []
        for r in self.records:
            days = (r.date.date() - self.base_date).days
            err = abs(r.real_weight - r.measured_weight) * 1000  # Error in grams
            X.append([days, r.real_weight, r.measured_weight])
            y.append(err)
        return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)
    
    def _build_model(self, input_dim=3):
        """Build neural network architecture"""
        model = Sequential([
            Dense(128, activation='relu', input_shape=(input_dim,)),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(1, activation='relu')  # Non-negative output
        ])
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        return model
    
    def _train(self, X, y):
        """Train the model with validation split"""
        self.model = self._build_model()
        
        # Callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=15,
                restore_best_weights=True,
                verbose=1
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-6,
                verbose=1
            )
        ]
        
        # Train
        history = self.model.fit(
            X, y,
            epochs=300,
            batch_size=16,
            validation_split=0.2,
            verbose=1,
            callbacks=callbacks
        )
        
        self.save()
        return history
    
    def predict(self, date, poids_attendu, poids_mesure):
        """Predict weight error for a given date and weights"""
        days = (date.date() if hasattr(date, 'date') else date - self.base_date).day
        X = np.array([[days, poids_attendu, poids_mesure]], dtype=np.float32)
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled, verbose=0)[0][0]
        return float(max(0, prediction))  # Ensure non-negative
    
    def predict_batch(self, dates, poids_attendus, poids_mesures):
        """Predict multiple errors at once (more efficient)"""
        days = np.array([(d.date() if hasattr(d, 'date') else d - self.base_date).day for d in dates])
        X = np.column_stack([days, poids_attendus, poids_mesures]).astype(np.float32)
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled, verbose=0).flatten()
        return np.maximum(0, predictions)  # Ensure non-negative
    
    def predict_tolerance_breach(self, tolerance, start_date, poids_attendu, 
                                poids_mesure, days_limit=30):
        """Find when error exceeds tolerance threshold"""
        dates = [start_date + timedelta(days=i) for i in range(days_limit)]
        poids_attendus = [poids_attendu] * days_limit
        poids_mesures = [poids_mesure] * days_limit
        
        predictions = self.predict_batch(dates, poids_attendus, poids_mesures)
        
        for i, pred in enumerate(predictions):
            if pred > tolerance:
                return dates[i]
        return None
    
    def evaluate(self, X=None, y=None):
        """Evaluate model performance"""
        if X is None or y is None:
            X = self.X_scaled
            _, y = self._prepare_data()
        
        y_pred = self.model.predict(X, verbose=0).flatten()
        
        mae = mean_absolute_error(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        mape = np.mean(np.abs((y - y_pred) / (y + 1e-8))) * 100  # Avoid division by zero
        
        return {
            "MAE": float(mae),
            "RMSE": float(rmse),
            "MAPE": float(mape)
        }
    
    def _update_metadata(self):
        """Save model metadata to JSON"""
        metrics = self.evaluate()
        metadata = {
            "model_name": "WeightErrorRegressor",
            "version": self.version,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dataset_size": len(self.records),
            "base_date": self.base_date.strftime("%Y-%m-%d"),
            "metrics": metrics,
            "seed": self.seed,
            "input_features": ["days_since_start", "expected_weight", "measured_weight"],
            "model_path": self.model_path,
            "scaler_path": self.scaler_path,
        }
        
        os.makedirs(os.path.dirname(self.metadata_path), exist_ok=True)
        with open(self.metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)
    
    def _save_scaler(self):
        """Persist scaler for consistent preprocessing"""
        import pickle
        os.makedirs(os.path.dirname(self.scaler_path), exist_ok=True)
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
    
    def save(self):
        """Save model and metadata"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
        self._save_scaler()
        self._update_metadata()
    
    def retrain(self):
        """Retrain model with fresh data from database"""
        session = next(get_db())
        try:
            self.records = session.query(Poids).order_by(Poids.date).all()
            if not self.records:
                raise ValueError("No weight records found in database")
        finally:
            session.close()
        
        X, y = self._prepare_data()
        y = y.reshape(-1, 1)
        self.X_scaled = self.scaler.fit_transform(X)
        
        return self._train(self.X_scaled, y)