import csv
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sklearn.linear_model import LinearRegression, SGDRegressor

# --- Configuration de la base de données ---
Base = declarative_base()

class Poids(Base):
    __tablename__ = 'poids'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    real_weight = Column(Float)
    measured_weight = Column(Float)
    tolerance = Column(Float, default=2.0)

class Resultat(Base):
    __tablename__ = 'resultats'
    id = Column(Integer, primary_key=True)
    predicted_date = Column(String)
    predicted_error = Column(Float)
    tolerance = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- Initialisation de la base de données ---
engine = create_engine('sqlite:///base_de_donnees.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# --- Insertion de données d'exemple ---
def inserer_donnees_exemple():
    if session.query(Poids).count() == 0:
        base_date = datetime(2023, 1, 1)
        real_weight = 70.0
        tolerance = 3000
        for i in range(10):
            date = base_date + timedelta(days=i)
            measured = real_weight + 0.2 * i
            p = Poids(date=date, real_weight=real_weight, measured_weight=measured, tolerance=tolerance)
            session.add(p)
        session.commit()
        print("✅ Données d'exemple insérées.")

# --- Prédiction ---
def predire_derivation(tolerance):
    records = session.query(Poids).order_by(Poids.date).all()
    if len(records) < 2:
        return None, None

    dates = [p.date for p in records]
    jours = np.array([(d - dates[0]).days for d in dates]).reshape(-1, 1)
    erreurs = np.array([abs(p.measured_weight - p.real_weight) * 1000 for p in records])  # en grammes

    model = LinearRegression()
    model.fit(jours, erreurs)

    if model.coef_[0] <= 0:
        return dates[-1], erreurs[-1]  # pas de dérive détectée

    jours_tolerance = (tolerance - model.intercept_) / model.coef_[0]

    if jours_tolerance < 0:
        return datetime.now(), erreurs[-1]

    predicted_date = dates[0] + timedelta(days=int(jours_tolerance))
    predicted_error = model.predict([[jours[-1][0]]])[0]

    return predicted_date, predicted_error



# --- Entrée de nouvelles données ---
def enter_data():
    try:
        date_input = input("Entrez la date (YYYY-MM-DD) : ").strip()
        date_obj = datetime.strptime(date_input, "%Y-%m-%d")
        real_weight = float(input("Entrez le poids réel (kg) : "))
        measured_weight = float(input("Entrez le poids mesuré (kg) : "))
        tolerance = float(input("Entrez la tolérance (g) : "))
    except ValueError:
        print("❌ Entrée invalide. Réessayez.")
        return

    error = abs(measured_weight - real_weight) * 1000  # en grammes

    poids = Poids(
        date=date_obj,
        real_weight=real_weight,
        measured_weight=measured_weight,
        tolerance=tolerance
    )
    session.add(poids)
    session.commit()

    print(f"📏 Erreur calculée : {error:.2f} g")

    predicted_date, predicted_error = predire_derivation(tolerance)
    if predicted_date:
        print(f"🔮 Date estimée de dépassement de tolérance : {predicted_date.date()}")
        print(f"📉 Erreur prédite ce jour-là : {predicted_error:.2f} g")

        res = Resultat(
            predicted_date=predicted_date.strftime("%Y-%m-%d"),
            predicted_error=predicted_error,
            tolerance=tolerance
        )
        session.add(res)
        session.commit()
    else:
        print("❌ Modèle non trouvé. Entraînement insuffisant (minimum 2 enregistrements).")

# --- Affichage des prédictions ---
def afficher_resultats():
    print("\n📊 Historique des prédictions :")
    resultats = session.query(Resultat).order_by(Resultat.created_at.desc()).all()
    if not resultats:
        print("Aucune prédiction enregistrée.")
        return
    for res in resultats:
        print(f"📅 {res.predicted_date} | Tolérance : {res.tolerance:.2f} g | Erreur prédite : {res.predicted_error:.2f} g | Ajouté le : {res.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

# --- Export CSV ---
def exporter_csv():
    resultats = session.query(Resultat).order_by(Resultat.created_at).all()
    if not resultats:
        print("⚠️ Aucun résultat à exporter.")
        return

    filename = f"historique_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Date Prédite", "Erreur Prédite (g)", "Tolérance (g)", "Créé le"])
        for r in resultats:
            writer.writerow([r.predicted_date, f"{r.predicted_error:.2f}", f"{r.tolerance:.2f}", r.created_at.strftime('%Y-%m-%d %H:%M:%S')])
    print(f"✅ Résultats exportés dans le fichier : {filename}")

# --- Menu principal ---
if __name__ == "__main__":
    inserer_donnees_exemple()

    while True:
        print("\n=== Menu ===")
        print("1. Entrer de nouvelles données")
        print("2. Afficher l'historique des prédictions")
        print("3. Exporter l'historique (CSV)")
        print("4. Quitter")

        choix = input("Votre choix : ").strip()
        if choix == "1":
            enter_data()
        elif choix == "2":
            afficher_resultats()
        elif choix == "3":
            exporter_csv()
        elif choix == "4":
            break
        else:
            print("❌ Choix invalide. Veuillez réessayer.")

    session.close()
