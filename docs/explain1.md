* Saisir **manuellement** :

  * le **poids réel de référence** (ex: 100 g),
  * le **poids mesuré par le capteur** (ex: 104.5 g),
  * une **tolérance** (ex: ±2 g),
* Et que le système :

  * détecte si l’écart dépasse la tolérance,
  * suive la dérive dans le temps,
  * **prédise à quel moment** l'erreur dépassera la tolérance (échéance estimée pour l'étalonnage).

---

## ✅ Vue d’ensemble du système :

### 📥 Données saisies à chaque mesure :

| Date       | Poids réel | Poids mesuré | Tolérance (g) |
| ---------- | ---------- | ------------ | ------------- |
| 2025-01-01 | 100        | 99.8         | 2             |
| 2025-02-01 | 100        | 101.1        | 2             |
| 2025-03-01 | 100        | 102.8        | 2             |

### 📊 Ce que l'app fait :

* Calcule **l’erreur = |poids mesuré - poids réel|**
* Compare l’erreur à la tolérance
* Enregistre une **alerte si l’erreur dépasse la tolérance**
* **Modélise la dérive dans le temps**
* Prédit **la date** à laquelle l’erreur dépassera la tolérance (si ce n’est pas déjà le cas)

---

## 🧠 Exemple de prédiction :

* Aujourd'hui, l’erreur est de 1.8 g (ok)
* L’erreur augmente de **0.5 g par mois**
* La tolérance est de 2 g
  → Il reste **0.2 g de marge**, soit \~12 jours avant dépassement