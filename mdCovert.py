import markdown
from pathlib import Path

# Charger le contenu du README.md
with open("./docs/ia.md", encoding="utf-8") as f:
    readme_content = f.read()

# Gabarit HTML avec Pico CSS (accolades échappées)
html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projet de Prédiction de Dérive de Poids</title>
    <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@1.5.10/css/pico.min.css">
    <style>
        body {{ padding: 2rem; }}
        pre {{ background: #f4f4f4; padding: 1rem; overflow-x: auto; }}
        code {{ font-family: monospace; color: #d63384; }}
        .badge img {{ vertical-align: middle; }}
    </style>
</head>
<body>
<main class="container">
{content}
</main>
</body>
</html>
"""

# Convertir le Markdown en HTML
html_content = markdown.markdown(
    readme_content,
    extensions=["extra", "codehilite", "toc"]
)

# Injecter dans le gabarit
final_html = html_template.format(content=html_content)

# Enregistrer dans un fichier
output_path = Path("ia.html")
output_path.write_text(final_html, encoding="utf-8")

print(f"✅ Fichier HTML généré : {output_path.absolute()}")
