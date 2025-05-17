
from app.compoments import Layout, Controls, NavBar
from .css import login_
from fasthtml.common import *
from ..compoments.base import BaseHtml 

class DashBord(Layout, Controls, NavBar):
    
    def __init__(self):
        super().__init__()
        
        self.html = BaseHtml(
            head=[
                Link(rel="stylesheet", href='../css/style.css'),
                Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
                Script(src='https://cdn.jsdelivr.net/npm/chart.js'),
                
            ],
            body=[
                self.nav(),
                H1("Résultats des Modèles"),
                Div(self.modeldiv('SGD Regretions LLM','1'), 
                    self.modeldiv('Lineare Regretions LLM','2'), 
                    self.modeldiv('Keras Multi Feature','3'), 
                    self.modeldiv('Keras Neural Network','4')
                    , cls='modelContainer'),
                self.jsContent()                
            ]

        )
    
    
    def modeldiv(self, name:str,canvasId:str):
        
        return Div(
            H2(f"{name}"),
            P(Strong(f"Date d'estimation : "),"2025-05-16", id=f"date{canvasId}"),
            P(Strong(f"Erreur prédite : "),"1.5 g", id=f"error{canvasId}"),
            P(Strong(f"Tolérance : "),"2.0 g", id=f"tolerance{canvasId}"),
            Canvas(id=f"chart{canvasId}"),
        )
    
    def jsContent(self):
        return Script(src='../js/dashbord.js')

    def page(self):
        return self.html.render()


def Index():
    return Html(
    Head(
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Title('Projet de Prédiction de Dérive de Poids'),
        Link(rel='stylesheet', href='https://unpkg.com/@picocss/pico@1.5.10/css/pico.min.css'),
        Style('body { padding: 2rem; }\r\n        pre { background: #f4f4f4; padding: 1rem; overflow-x: auto; }\r\n        code { font-family: monospace; color: #d63384; }\r\n        .badge img { vertical-align: middle; }')
    ),
    Body(
        Main(
            H1('🎯 Projet de Prédiction de Dérive de Poids', id='projet-de-prediction-de-derive-de-poids'),
            Br(),
            H2('go to dashbord ',A(href='/dashbord')),
            P(
                A(
                    Img(alt='Python', src='https://img.shields.io/badge/python-3.11%2B-blue'),
                    href='https://www.python.org/'
                ),
                A(
                    Img(alt='License: MIT', src='https://img.shields.io/badge/license-MIT-green.svg'),
                    href='./LICENCE'
                ),
                A(
                    Img(alt='FastAPI', src='https://img.shields.io/badge/FastAPI-🚀-green'),
                    href='https://fastapi.tiangolo.com/'
                ),
                A(
                    Img(alt='Made with TensorFlow', src='https://img.shields.io/badge/Made%20with-TensorFlow-orange'),
                    href='https://www.tensorflow.org/'
                ),
                A(
                    Img(alt='Made with Keras', src='https://img.shields.io/badge/Made%20with-Keras-orange'),
                    href='https://keras.io/'
                ),
                A(
                    Img(alt='Made with scikit-learn', src='https://img.shields.io/badge/Made%20with-scikit-learn-orange'),
                    href='https://scikit-learn.org/'
                ),
                A(
                    Img(alt='Made with uvicorn', src='https://img.shields.io/badge/Made%20with-uvicorn-orange'),
                    href='https://www.uvicorn.org/'
                ),
                A(
                    Img(alt='Chart.js', src='https://img.shields.io/badge/Chart.js-📊-blueviolet'),
                    href='https://www.chartjs.org/'
                ),
                A(
                    Img(alt='Status', src='https://img.shields.io/badge/status-en%20cours-yellow'),
                    href=''
                ),
                Br(),
                'Ce projet vise à',
                Strong('prédire la dérive de poids'),
                'à l’aide de modèles d’apprentissage automatique, et à',
                Strong('visualiser dynamiquement'),
                'les résultats via un dashboard web.'
            ),
            Hr(),
            H2('⚙️ Technologies utilisées', id='technologies-utilisees'),
            H3('Backend', id='backend'),
            Ul(
                Li(
                    Strong('Python 3.11+')
                ),
                Li(
                    Strong('FastAPI (fasthtml)'),
                    '– Création rapide d’API'
                ),
                Li(
                    Strong('SQLAlchemy'),
                    '– ORM pour manipuler la base de données'
                ),
                Li(
                    Strong('Pydantic'),
                    '– Validation des données entrantes/sortantes'
                ),
                Li(
                    Strong('TensorFlow / Keras'),
                    '– Réseaux de neurones pour la prédiction'
                ),
                Li(
                    Strong('scikit-learn'),
                    '– Régression linéaire et autres modèles'
                ),
                Li(
                    Strong('uvicorn'),
                    '– Serveur ASGI ultra rapide'
                )
            ),
            H3('Frontend', id='frontend'),
            Ul(
                Li(
                    Strong('HTML / CSS / JavaScript')
                ),
                Li(
                    Strong('Chart.js'),
                    '– Visualisation des erreurs prédictives'
                ),
                Li(
                    Strong('Fetch API'),
                    '– Requêtes AJAX régulières pour actualiser les graphiques'
                )
            ),
            Hr(),
            H2('🚀 Lancement du projet', id='lancement-du-projet'),
            H3('1. Cloner le dépôt', id='1-cloner-le-depot'),
            Div(
                Pre(
                    Span(),
                    Code(
                        'git',
                        Span(cls='w'),
                        'clone',
                        Span(cls='w'),
                        'https://github.com/mon-utilisateur/poids-drift-project.git',
                        Span('cd', cls='nb'),
                        Span(cls='w'),
                        'poids-drift-project'
                    )
                ),
                cls='codehilite'
            ),
            H3('2. Installer les dépendances', id='2-installer-les-dependances'),
            Div(
                Pre(
                    Span(),
                    Code(
                        'pip',
                        Span(cls='w'),
                        'install',
                        Span(cls='w'),
                        '-r',
                        Span(cls='w'),
                        'requirements.txt'
                    )
                ),
                cls='codehilite'
            ),
            H3('3. Lancer le serveur', id='3-lancer-le-serveur'),
            Div(
                Pre(
                    Span(),
                    Code(
                        'uvicorn',
                        Span(cls='w'),
                        'main:app',
                        Span(cls='w'),
                        '--reload'
                    )
                ),
                cls='codehilite'
            ),
            H3('4. Accéder au dashboard', id='4-acceder-au-dashboard'),
            P('Ouvrir dans le navigateur :'),
            Div(
                Pre(
                    Span(),
                    Code('http://localhost:8000/dashboard')
                ),
                cls='codehilite'
            ),
            Hr(),
            H2('🔄 Fonctionnement', id='fonctionnement'),
            Ol(
                Li('L’utilisateur soumet un poids réel, un poids mesuré et une tolérance.'),
                Li('Plusieurs modèles (ML, Deep Learning) calculent les erreurs de prédiction.'),
                Li('Les résultats sont stockés en base de données.'),
                Li(
                    'Le frontend (Chart.js) interroge les API toutes les',
                    Strong('6 secondes'),
                    ':'
                )
            ),
            Div(
                Pre(
                    Span(),
                    Code('/models/model1/\r\n/models/model2/\r\n/models/model3/\r\n/models/model4/')
                ),
                cls='codehilite'
            ),
            P('Chacune retourne :'),
            Div(
                Pre(
                    Span(),
                    Code(
                        Span('{', cls='p'),
                        Span(cls='w'),
                        Span('"error"', cls='nt'),
                        Span(':', cls='p'),
                        Span(cls='w'),
                        Span('[', cls='p'),
                        Span('1.2', cls='mf'),
                        Span(',', cls='p'),
                        Span(cls='w'),
                        Span('1.3', cls='mf'),
                        Span(',', cls='p'),
                        Span(cls='w'),
                        Span('1.1', cls='mf'),
                        Span(',', cls='p'),
                        Span(cls='w'),
                        Span('...', cls='err'),
                        Span('],', cls='p'),
                        Span(cls='w'),
                        Span('"data"', cls='nt'),
                        Span(':', cls='p'),
                        Span(cls='w'),
                        Span('[', cls='p'),
                        Span('1.5', cls='mf'),
                        Span(',', cls='p'),
                        Span(cls='w'),
                        Span('1.6', cls='mf'),
                        Span(',', cls='p'),
                        Span(cls='w'),
                        Span('1.8', cls='mf'),
                        Span(',', cls='p'),
                        Span(cls='w'),
                        Span('...', cls='err'),
                        Span(']', cls='p'),
                        Span('}', cls='p')
                    )
                ),
                cls='codehilite'
            ),
            Hr(),
            H2('📊 Visualisation (Dashboard)', id='visualisation-dashboard'),
            Ul(
                Li('Chaque graphique représente un modèle.'),
                Li('Les erreurs sont affichées mois par mois.'),
                Li(
                    'Les données sont rafraîchies automatiquement toutes les 6 secondes via',
                    Code('fetch()'),
                    '.'
                )
            ),
            Hr(),
            H2('📦 Exemple de modèle de prédiction', id='exemple-de-modele-de-prediction'),
            Div(
                Pre(
                    Span(),
                    Code(
                        Span('from', cls='kn'),
                        Span(cls='w'),
                        Span('keras.models', cls='nn'),
                        Span(cls='w'),
                        Span('import', cls='kn'),
                        Span('Sequential', cls='n'),
                        Span('from', cls='kn'),
                        Span(cls='w'),
                        Span('keras.layers', cls='nn'),
                        Span(cls='w'),
                        Span('import', cls='kn'),
                        Span('Dense', cls='n'),
                        Span('model', cls='n'),
                        Span('=', cls='o'),
                        Span('Sequential', cls='n'),
                        Span('([', cls='p'),
                        Span('Dense', cls='n'),
                        Span('(', cls='p'),
                        Span('64', cls='mi'),
                        Span(',', cls='p'),
                        Span('activation', cls='n'),
                        Span('=', cls='o'),
                        Span("'relu'", cls='s1'),
                        Span(',', cls='p'),
                        Span('input_shape', cls='n'),
                        Span('=', cls='o'),
                        Span('(', cls='p'),
                        Span('3', cls='mi'),
                        Span(',)),', cls='p'),
                        Span('Dense', cls='n'),
                        Span('(', cls='p'),
                        Span('32', cls='mi'),
                        Span(',', cls='p'),
                        Span('activation', cls='n'),
                        Span('=', cls='o'),
                        Span("'relu'", cls='s1'),
                        Span('),', cls='p'),
                        Span('Dense', cls='n'),
                        Span('(', cls='p'),
                        Span('1', cls='mi'),
                        Span(')', cls='p'),
                        Span('])', cls='p'),
                        Span('model', cls='n'),
                        Span('.', cls='o'),
                        Span('compile', cls='n'),
                        Span('(', cls='p'),
                        Span('optimizer', cls='n'),
                        Span('=', cls='o'),
                        Span("'adam'", cls='s1'),
                        Span(',', cls='p'),
                        Span('loss', cls='n'),
                        Span('=', cls='o'),
                        Span("'mse'", cls='s1'),
                        Span(')', cls='p')
                    )
                ),
                cls='codehilite'
            ),
            Hr(),
            H2('✅ Fonctionnalités', id='fonctionnalites'),
            Ul(
                Li('[x] Prédiction en temps réel de la dérive de poids'),
                Li('[x] Sauvegarde automatique des résultats'),
                Li('[x] Dashboard interactif mis à jour régulièrement'),
                Li('[x] Support multi-modèles'),
                Li('[x] Authentification avec JWT')
            ),
            Hr(),
            H2('🔒 Sécurité', id='securite'),
            Ul(
                Li('Authentification via tokens JWT'),
                Li('Protection des endpoints sensibles'),
                Li(
                    'Gestion des utilisateurs dans',
                    Code('models/admin.py')
                )
            ),
            Hr(),
            H2('📚 Documentation', id='documentation'),
            P('Les fichiers suivants apportent des détails techniques :'),
            Ul(
                Li(
                    Code('docs/explain1.md'),
                    '– Description générale du projet',
                    A('[1]', href='./docs/explain1.md')
                ),
                Li(
                    Code('docs/ia.md'),
                    "– Détails sur les modèles d'intelligence artificielle utilisés",
                    A('[2]', href='./docs/ia.md')
                )
            ),
            Hr(),
            H2('🔧 Améliorations futures', id='ameliorations-futures'),
            Ul(
                Li("🔐 Système d'utilisateurs avec rôles"),
                Li('🧾 Export CSV / Excel / PDF des résultats'),
                Li('📈 Visualisation des performances historiques'),
                Li('🧠 Intégration de nouveaux modèles LLM ou hybrides')
            ),
            Hr(),
            H2('🧑\u200d💻 Auteurs', id='auteurs'),
            Ul(
                Li(
                    Strong('👤 Myriade Technologie')
                ),
                Li(
                    '📧',
                    A('traoreera@gmail.com', href='mailto:traoreera@gmail.com')
                )
            ),
            Hr(),
            H2('🪪 Licence', id='licence'),
            P(
                'Ce projet est open-source sous licence',
                Strong('MIT'),
                '.\r\nVoir',
                A(
                    Code('LICENCE.md'),
                    href='./LICENCE'
                ),
                'pour plus d’informations.'
            ),
            cls='container'
        )
    ),
    lang='fr'
)


def license():
    
    return Html(
    Head(
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Title('Projet de Prédiction de Dérive de Poids'),
        Link(rel='stylesheet', href='https://unpkg.com/@picocss/pico@1.5.10/css/pico.min.css'),
        Style('body { padding: 2rem; }\r\n        pre { background: #f4f4f4; padding: 1rem; overflow-x: auto; }\r\n        code { font-family: monospace; color: #d63384; }\r\n        .badge img { vertical-align: middle; }')
    ),
    Body(
        Main(
            P(
                'Licence MIT Modifiée – Usage Restreint',
                Br(),
                'Copyright (c) 2025 Myriade Technologie'
            ),
            P('Permission est accordée, gratuitement, à toute personne obtenant une copie du présent logiciel et des fichiers de documentation associés (le « Logiciel »), de l’utiliser, de le copier, de le modifier et de le distribuer, sous réserve des conditions suivantes :'),
            Ol(
                Li(
                    P(
                        Strong('Utilisation personnelle, académique et non commerciale uniquement.'),
                        'Le Logiciel peut être utilisé à des fins personnelles, éducatives ou de recherche',
                        Strong('non commerciales'),
                        '.',
                        Br(),
                        'Toute utilisation',
                        Strong('commerciale'),
                        ', y compris la revente, la location ou l’intégration dans un produit commercial, est',
                        Strong('strictement interdite sans autorisation écrite préalable'),
                        'de Myriade Technologie.'
                    )
                ),
                Li(
                    P(
                        Strong('Interdiction d’usage militaire ou de surveillance.'),
                        'Le Logiciel ne peut pas être utilisé, directement ou indirectement, pour des fins militaires, de surveillance massive, de reconnaissance faciale, ou tout système pouvant porter atteinte aux droits humains fondamentaux.'
                    )
                ),
                Li(
                    P(
                        Strong('Mention obligatoire du copyright.'),
                        'Le présent avis de droit d’auteur ainsi que les conditions de licence doivent être inclus dans toutes les copies ou parties substantielles du Logiciel.'
                    )
                ),
                Li(
                    P(
                        Strong('Aucune garantie.'),
                        "Le Logiciel est fourni « tel quel », sans aucune garantie, expresse ou implicite, y compris mais sans s’y limiter les garanties de qualité marchande, d’adéquation à un usage particulier et d’absence de contrefaçon. En aucun cas les auteurs ou titulaires du droit d’auteur ne pourront être tenus responsables de toute réclamation, dommage ou autre responsabilité, que ce soit dans le cadre d’une action contractuelle, délictuelle ou autre, découlant de, ou en rapport avec, le Logiciel ou l’utilisation ou d'autres relations avec le Logiciel."
                    )
                )
            ),
            Hr(),
            P(
                'Pour toute demande d’usage commercial, veuillez contacter :',
                Br(),
                '📧 traoreera@gmail.com'
            ),
            cls='container'
        )
    ),
    lang='fr'
)


def explain():
    return Html(
    Head(
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Title('Projet de Prédiction de Dérive de Poids'),
        Link(rel='stylesheet', href='https://unpkg.com/@picocss/pico@1.5.10/css/pico.min.css'),
        Style('body { padding: 2rem; }\r\n        pre { background: #f4f4f4; padding: 1rem; overflow-x: auto; }\r\n        code { font-family: monospace; color: #d63384; }\r\n        .badge img { vertical-align: middle; }')
    ),
    Body(
        Main(
            Ul(
                Li(
                    P(
                        'Saisir',
                        Strong('manuellement'),
                        ':'
                    )
                ),
                Li(
                    P(
                        'le',
                        Strong('poids réel de référence'),
                        '(ex: 100 g),'
                    )
                ),
                Li(
                    'le',
                    Strong('poids mesuré par le capteur'),
                    '(ex: 104.5 g),'
                ),
                Li(
                    'une',
                    Strong('tolérance'),
                    '(ex: ±2 g),'
                ),
                Li(
                    P('Et que le système :')
                ),
                Li(
                    P('détecte si l’écart dépasse la tolérance,')
                ),
                Li('suive la dérive dans le temps,'),
                Li(
                    Strong('prédise à quel moment'),
                    "l'erreur dépassera la tolérance (échéance estimée pour l'étalonnage)."
                )
            ),
            Hr(),
            H2('✅ Vue d’ensemble du système :', id='vue-densemble-du-systeme'),
            H3('📥 Données saisies à chaque mesure :', id='donnees-saisies-a-chaque-mesure'),
            Table(
                Thead(
                    Tr(
                        Th('Date'),
                        Th('Poids réel'),
                        Th('Poids mesuré'),
                        Th('Tolérance (g)')
                    )
                ),
                Tbody(
                    Tr(
                        Td('2025-01-01'),
                        Td('100'),
                        Td('99.8'),
                        Td('2')
                    ),
                    Tr(
                        Td('2025-02-01'),
                        Td('100'),
                        Td('101.1'),
                        Td('2')
                    ),
                    Tr(
                        Td('2025-03-01'),
                        Td('100'),
                        Td('102.8'),
                        Td('2')
                    )
                )
            ),
            H3("📊 Ce que l'app fait :", id='ce-que-lapp-fait'),
            Ul(
                Li(
                    'Calcule',
                    Strong('l’erreur = |poids mesuré - poids réel|')
                ),
                Li('Compare l’erreur à la tolérance'),
                Li(
                    'Enregistre une',
                    Strong('alerte si l’erreur dépasse la tolérance')
                ),
                Li(
                    Strong('Modélise la dérive dans le temps')
                ),
                Li(
                    'Prédit',
                    Strong('la date'),
                    'à laquelle l’erreur dépassera la tolérance (si ce n’est pas déjà le cas)'
                )
            ),
            Hr(),
            H2('🧠 Exemple de prédiction :', id='exemple-de-prediction'),
            Ul(
                Li("Aujourd'hui, l’erreur est de 1.8 g (ok)"),
                Li(
                    'L’erreur augmente de',
                    Strong('0.5 g par mois')
                ),
                Li(
                    'La tolérance est de 2 g\r\n  → Il reste',
                    Strong('0.2 g de marge'),
                    ', soit \\~12 jours avant dépassement'
                )
            ),
            cls='container'
        )
    ),
    lang='fr'
)


def ia():
    return Html(
    Head(
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Title('Projet de Prédiction de Dérive de Poids'),
        Link(rel='stylesheet', href='https://unpkg.com/@picocss/pico@1.5.10/css/pico.min.css'),
        Style('body { padding: 2rem; }\r\n        pre { background: #f4f4f4; padding: 1rem; overflow-x: auto; }\r\n        code { font-family: monospace; color: #d63384; }\r\n        .badge img { vertical-align: middle; }')
    ),
    Body(
        Main(
            P(
                'Dans ce script, il y a',
                Strong('une forme simple d’intelligence artificielle'),
                ': une',
                Strong('régression linéaire'),
                '.'
            ),
            Hr(),
            H3("📌 Où est le modèle d'IA ?", id='ou-est-le-modele-dia'),
            P(
                'La ligne suivante utilise',
                Strong(
                    Code('LinearRegression()')
                ),
                'de',
                Strong('scikit-learn'),
                ':'
            ),
            Div(
                Pre(
                    Span(),
                    Code(
                        Span('model', cls='n'),
                        Span('=', cls='o'),
                        Span('LinearRegression', cls='n'),
                        Span('()', cls='p'),
                        Span('model', cls='n'),
                        Span('.', cls='o'),
                        Span('fit', cls='n'),
                        Span('(', cls='p'),
                        Span('jours', cls='n'),
                        Span(',', cls='p'),
                        Span('erreurs', cls='n'),
                        Span(')', cls='p')
                    )
                ),
                cls='codehilite'
            ),
            P(
                'Ce modèle apprend la',
                Strong('relation entre le temps (en jours)'),
                'et',
                Strong('l’erreur de mesure (en grammes)'),
                '. Il essaie de',
                Strong('prédire'),
                'quand l’erreur atteindra la',
                Strong('tolérance maximale définie'),
                '.'
            ),
            Hr(),
            H3('🤖 Pourquoi c’est une IA ?', id='pourquoi-cest-une-ia'),
            P(
                'Même si ce n’est pas une IA complexe comme un réseau de neurones, c’est un modèle',
                Strong('d’apprentissage supervisé'),
                ':'
            ),
            Ul(
                Li(
                    Strong("Données d'entrée"),
                    ': la date (convertie en nombre de jours).'
                ),
                Li(
                    Strong('Données de sortie'),
                    ': l’erreur (écart entre le poids mesuré et le poids réel).'
                ),
                Li(
                    'Le modèle',
                    Strong('apprend une tendance'),
                    '(la dérive des erreurs).'
                ),
                Li(
                    'Il peut ensuite',
                    Strong('prédire dans le futur'),
                    '(date de dépassement de tolérance).'
                )
            ),
            Hr(),
            H3('🎯 Exemple d’usage de l’IA ici', id='exemple-dusage-de-lia-ici'),
            Blockquote(
                P('Si les erreurs augmentent chaque jour (0.2 kg par exemple), l’IA prévoit à quelle date l’erreur atteindra la limite tolérée (3000 g ici). C’est utile dans la maintenance ou le recalibrage d’un système.')
            ),
            Hr(),
            cls='container'
        )
    ),
    lang='fr'
)