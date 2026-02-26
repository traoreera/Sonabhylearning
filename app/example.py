from app.models import Poids
from datetime import datetime, timedelta
from app.database import get_db
import random
session = next(get_db())



def inserer_donnees_exemple(len_data: int = 365):
    if session.query(Poids).count() > 0:
        print("⚠️ Données déjà existantes, insertion ignorée.")
        return
    
    base_date = datetime(2024, 1, 1)

    real_weight_start = 70.0     # poids initial en kg
    drift_rate = random.uniform(-0.01, 0.02)   # dérive réaliste
    tolerance = 0.15             # en kg
    objectif = 72.0              # cible utilisateur

    for i in range(len_data):
        date = base_date + timedelta(days=i)

        # Simule un poids réel variant autour du trend
        real_weight = real_weight_start + (drift_rate * i)

        # Ajout bruit aléatoire du capteur
        noise = random.uniform(-0.05, 0.05)

        measured = real_weight + noise

        p = Poids(
            date=date,
            real_weight=round(real_weight, 3),
            measured_weight=round(measured, 3),
            tolerance=tolerance,
        )
        session.add(p)

    session.commit()
    print(f"✅ {len_data} mesures simulées avec dérive {drift_rate:.4f} kg/jour.")
