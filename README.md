# 🎯 Projet de Prédiction de Dérive de Poids
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENCE.md)
[![FastAPI](https://img.shields.io/badge/FastAPI-🚀-green)](https://fastapi.tiangolo.com/)
[![Made with TensorFlow](https://img.shields.io/badge/Made%20with-TensorFlow-orange)](https://www.tensorflow.org/)
[![Made with Keras](https://img.shields.io/badge/Made%20with-Keras-orange)](https://keras.io/)
[![Made with scikit-learn](https://img.shields.io/badge/Made%20with-scikit-learn-orange)](https://scikit-learn.org/)
[![Made with uvicorn](https://img.shields.io/badge/Made%20with-uvicorn-orange)](https://www.uvicorn.org/)
[![Chart.js](https://img.shields.io/badge/Chart.js-📊-blueviolet)](https://www.chartjs.org/)
[![Status](https://img.shields.io/badge/status-en%20cours-yellow)]() <br>
Ce projet vise à **prédire la dérive de poids** à l’aide de modèles d’apprentissage automatique, et à **visualiser dynamiquement** les résultats via un dashboard web.

---

## 🗂️ Structure du projet

```
.
├── app/                      # Code principal de l'application
│   ├── auth/                # Authentification JWT, gestion des tokens
│   ├── compoments/          # Composants UI pour l’interface
│   ├── core/                # Fonctions principales, modèles ML (Keras)
│   ├── db/                  # Schémas Pydantic & opérations CRUD
│   ├── models/              # Modèles SQLAlchemy (Poids, Résultats, Admin)
│   ├── pages/               # Templates HTML et logique associée
│   ├── routes/              # Endpoints FastAPI pour l’auth, les modèles, etc.
│   └── settings/            # Configuration centrale de l’application
├── static/                  # Ressources statiques (CSS, JS)
├── docs/                    # Documentation technique du projet
├── initdb.py                # Script d’initialisation de la base de données
├── runLLM.py                # Lancement des modèles de prédiction
├── task.py                  # Tâches automatisées ou périodiques
├── main.py                  # Point d’entrée principal de l’application
├── base_de_donnees.db       # Base de données SQLite
├── requirements.txt         # Dépendances Python
├── README.md                # Ce fichier
└── LICENCE.md               # Licence du projet
```

---

## ⚙️ Technologies utilisées

### Backend

* **Python 3.11+**
* **FastAPI (fasthtml)** – Création rapide d’API
* **SQLAlchemy** – ORM pour manipuler la base de données
* **Pydantic** – Validation des données entrantes/sortantes
* **TensorFlow / Keras** – Réseaux de neurones pour la prédiction
* **scikit-learn** – Régression linéaire et autres modèles
* **uvicorn** – Serveur ASGI ultra rapide

### Frontend

* **HTML / CSS / JavaScript**
* **Chart.js** – Visualisation des erreurs prédictives
* **Fetch API** – Requêtes AJAX régulières pour actualiser les graphiques

---

## 🚀 Lancement du projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/mon-utilisateur/poids-drift-project.git
cd poids-drift-project
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer le serveur

```bash
uvicorn main:app --reload
```

### 4. Accéder au dashboard

Ouvrir dans le navigateur :

```
http://localhost:8000/dashboard
```

---

## 🔄 Fonctionnement

1. L’utilisateur soumet un poids réel, un poids mesuré et une tolérance.
2. Plusieurs modèles (ML, Deep Learning) calculent les erreurs de prédiction.
3. Les résultats sont stockés en base de données.
4. Le frontend (Chart.js) interroge les API toutes les **6 secondes** :

```
/models/model1/
/models/model2/
/models/model3/
/models/model4/
```

Chacune retourne :

```json
{
  "error": [1.2, 1.3, 1.1, ...],
  "data": [1.5, 1.6, 1.8, ...]
}
```

---

## 📊 Visualisation (Dashboard)

* Chaque graphique représente un modèle.
* Les erreurs sont affichées mois par mois.
* Les données sont rafraîchies automatiquement toutes les 6 secondes via `fetch()`.

---

## 📦 Exemple de modèle de prédiction

```python
from keras.models import Sequential
from keras.layers import Dense

model = Sequential([
    Dense(64, activation='relu', input_shape=(3,)),
    Dense(32, activation='relu'),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')
```

---

## ✅ Fonctionnalités

* [x] Prédiction en temps réel de la dérive de poids
* [x] Sauvegarde automatique des résultats
* [x] Dashboard interactif mis à jour régulièrement
* [x] Support multi-modèles
* [x] Authentification avec JWT

---

## 🔒 Sécurité

* Authentification via tokens JWT
* Protection des endpoints sensibles
* Gestion des utilisateurs dans `models/admin.py`

---

## 📚 Documentation

Les fichiers suivants apportent des détails techniques :

* `docs/explain1.md` – Description générale du projet [[1]](./docs/explain1.md)
* `docs/ia.md` – Détails sur les modèles d'intelligence artificielle utilisés [[2]](./docs/ia.md)

---

## 🔧 Améliorations futures

* 🔐 Système d'utilisateurs avec rôles
* 🧾 Export CSV / Excel / PDF des résultats
* 📈 Visualisation des performances historiques
* 🧠 Intégration de nouveaux modèles LLM ou hybrides

---

## 🧑‍💻 Auteurs

* **👤 Myriade Technologie**
* 📧 [traoreera@gmail.com](mailto:traoreera@gmail.com)

---

## 🪪 Licence

Ce projet est open-source sous licence **MIT**.
Voir [`LICENCE.md`](./LICENCE.md) pour plus d’informations.
