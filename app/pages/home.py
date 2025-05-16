
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