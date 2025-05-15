
# 📦 Prédiction de Dérive de Poids avec Apprentissage Automatique

Ce projet utilise des modèles de régression (linéaire et SGD) pour estimer la date à laquelle l'erreur entre le poids mesuré et le poids réel dépassera une certaine **tolérance** en grammes.

## 📚 Fonctionnalités

- 📈 Régression linéaire (`LinearRegression`)
- ⚙️ Régression stochastique (`SGDRegressor`)
- 🧠 Modèles entraînés sur des données enregistrées en base de données (SQLAlchemy)
- 📅 Estimation de la date de dépassement de tolérance
- 💾 Sauvegarde automatique des modèles dans `./LLMmodels/`

---

## 🔧 Dépendances

Assurez-vous d'avoir les bibliothèques suivantes installées :

```bash
pip install tensorflow matplotlib numpy uvicorn[standard] sqlalchemy psycopg2-binary python-dotenv alembic passlib[bcrypt] gunicorn python-jose pydentic python-fasthtml apscheduler pandas
````

---

## 🧠 Modèles utilisés

### Linear Regression

```python
from sklearn.linear_model import LinearRegression
```

* Apprentissage complet à chaque appel
* Sauvegarde du modèle dans `./LLMmodels/LineareRegretion.pkl`

### SGD Regressor

```python
from sklearn.linear_model import SGDRegressor
```

* Apprentissage incrémental avec `partial_fit`
* Sauvegarde dans `./LLMmodels/sgdRegretion.pkl`

---

## ⚙️ Utilisation des fonctions

### 1. `LineareRegretion(tolerance: int) -> (datetime, float)`

Prédit la date de dépassement de la tolérance à l'aide d'une régression linéaire.

### 2. `SGDRegretions(tolerance: int) -> (datetime, float)`

Pareil mais avec régression SGD (entraînement incrémental).

---

## 🧪 Exemple d'exécution

```python
tolerance = 3000  # en grammes
date_predite, erreur_predite = LineareRegretion(tolerance)
print(f"📅 Dépassement estimé le {date_predite} avec une erreur de {erreur_predite:.2f} g")
```

---

## 🛠 Pré-requis

* Base de données contenant des objets `Poids`
* Champs requis : `date`, `real_weight`, `measured_weight`, `tolerance`

---

## 📌 Avertissement

> Les modèles ne fonctionneront correctement que si les données suivent une tendance croissante ou décroissante significative de l’erreur. Les modèles ne détecteront **aucune dérive** si les erreurs sont aléatoires ou stables.

---

## 📬 Contributeurs

* 🤖 Modèle de régression : scikit-learn
* 🧑‍💻 Auteur : \[traoreera]
