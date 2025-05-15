Dans ce script, il y a **une forme simple d’intelligence artificielle** : une **régression linéaire**.

---

### 📌 Où est le modèle d'IA ?

La ligne suivante utilise **`LinearRegression()`** de **scikit-learn** :

```python
model = LinearRegression()
model.fit(jours, erreurs)
```

Ce modèle apprend la **relation entre le temps (en jours)** et **l’erreur de mesure (en grammes)**. Il essaie de **prédire** quand l’erreur atteindra la **tolérance maximale définie**.

---

### 🤖 Pourquoi c’est une IA ?

Même si ce n’est pas une IA complexe comme un réseau de neurones, c’est un modèle **d’apprentissage supervisé** :

* **Données d'entrée** : la date (convertie en nombre de jours).
* **Données de sortie** : l’erreur (écart entre le poids mesuré et le poids réel).
* Le modèle **apprend une tendance** (la dérive des erreurs).
* Il peut ensuite **prédire dans le futur** (date de dépassement de tolérance).

---

### 🎯 Exemple d’usage de l’IA ici

> Si les erreurs augmentent chaque jour (0.2 kg par exemple), l’IA prévoit à quelle date l’erreur atteindra la limite tolérée (3000 g ici). C’est utile dans la maintenance ou le recalibrage d’un système.

---