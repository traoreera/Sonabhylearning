from app.models.poids import Poids
from datetime import datetime, timedelta
from app.models.database import get_db
import random
session = next(get_db())

# --- Insertion de données d'exemple ---
def inserer_donnees_exemple(len_data:int = 365):
    if session.query(Poids).count() == 0:
        base_date = datetime(2023, 1, 1)
        real_weight = 70.0
        tolerance = 3000
        for i in range(len_data):
            date = base_date + timedelta(days=i)
            measured = real_weight + 0.2 * i
            p = Poids(date=date, real_weight=real_weight, measured_weight=measured, tolerance=tolerance)
            session.add(p)
        session.commit()
        print("✅ Données d'exemple insérées.")





def inserer_donnees_exemple_variees(len_data: int = 365, real_weight: float = 70.0, max_drift_kg: float = 15.0):
    if session.query(Poids).count() == 0:
        base_date = datetime(2023, 1, 1)
        tolerance = 3000  # en grammes

        for i in range(len_data):
            date = base_date + timedelta(days=i)

            # Dérive progressive non-linéaire + bruit aléatoire
            drift_factor = (i / len_data)  # entre 0 et 1
            drift = drift_factor * max_drift_kg  # poids dérivé progressif
            noise = random.uniform(-0.1, 0.1)  # bruit aléatoire (±100g)

            measured_weight = real_weight + drift + noise

            p = Poids(
                date=date,
                real_weight=real_weight,
                measured_weight=measured_weight,
                tolerance=tolerance
            )
            session.add(p)

        session.commit()
        print("✅ Données variées insérées.")
    else:
        print("ℹ️ La base contient déjà des données. Aucune insertion effectuée.")
