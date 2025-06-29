import json
import re
from datetime import datetime
from collections import defaultdict

# 📁 Entrée/sortie
fichier_entree = "data.yml"            # ton fichier brut (texte ou csv avec 1 valeur par ligne)
fichier_json_sortie = "donnees.json"   # fichier JSON généré

# 🔁 Lire et nettoyer le fichier
with open(fichier_entree, "r", encoding="utf-8") as f:
    lignes = [l.strip().replace(",", "") for l in f if l.strip()]

# 🔎 Dictionnaire mois FR → EN
mois_fr_to_en = {
    "janvier": "Jan", "février": "Feb", "fevrier": "Feb",
    "mars": "Mar", "avril": "Apr", "mai": "May", "juin": "Jun",
    "juillet": "Jul", "août": "Aug", "aout": "Aug",
    "septembre": "Sep", "octobre": "Oct",
    "novembre": "Nov", "décembre": "Dec", "decembre": "Dec"
}

# 📦 Transformation en dict JSON
resultat = defaultdict(list)
date_actuelle = None

for ligne in lignes:
    if "poids obtenu" in ligne.lower():
        match = re.search(r"le\s+(\d{1,2})\s+(\w+)\s+(\d{4})", ligne.lower())
        if match:
            jour, mois_fr, annee = match.groups()
            mois_en = mois_fr_to_en.get(mois_fr.strip())
            if mois_en:
                date = datetime.strptime(f"{annee}-{mois_en}-{jour}", "%Y-%b-%d")
                date_actuelle = date.strftime("%Y-%m-%d")
            else:
                print(f"⚠️ Mois non reconnu : {mois_fr}")
                date_actuelle = None
    elif date_actuelle:
        try:
            valeur = float(ligne)
            resultat[date_actuelle].append(valeur)
        except ValueError:
            print(f"⛔ Ligne ignorée (non numérique) : {ligne}")

# 💾 Sauvegarder en JSON
with open(fichier_json_sortie, "w", encoding="utf-8") as f:
    json.dump(resultat, f, indent=4, ensure_ascii=False)

print(f"✅ Données converties et sauvegardées dans : {fichier_json_sortie}")
