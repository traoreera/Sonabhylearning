from fasthtml.common import *


class NavConf:

    dashbord = {"title": "Dashboard", "icon": "📊","links": [{"name": "Aperçu général", "path": "/"}]}

    user = {"title": "Gestion des Utilisateurs", "icon": "👤", "links": [
        {"name": "Liste des utilisateurs", "path": "/users"},
        {"name": "Ajouter un utilisateur", "path": "/users/add"}
    ]}
    api = {"title": "models", "icon": "🔑", "links": [
        {"name": "Liste des modèles", "path": "/models"},
        {"name": "Modifier un modèle", "path": "/models/edit"},
        {"name": "Ajouter un modèle", "path": "/models/add"}
    ]}


class NavBar:
    def __init___(self):

        super().__init__()

        return

    def nav(self, page: str = 'App'):
        return Nav(Ul(Li(Strong(f"{page}"), Li(I(), id='theme_switcher',))),
        Ul(
            Li(self.summary(dashorditems=NavConf.dashbord)),
            Li(self.summary(dashorditems=NavConf.user)),
            Li(self.summary(dashorditems=NavConf.api)),
        ),
            style="""
                        position: sticky;
                        top: 0;"""
        )

    def summary(self, dashorditems: dict = NavConf.user):

        list_dict = {link['name']: link['path']
        for link in dashorditems['links']}
        li_list = [Li(A(key, href=value)) for key, value in list_dict.items()]
        ul = Ul(*li_list, dir='rtl')
        return Details(Summary(f"{dashorditems['icon']} {dashorditems['title']}"), ul, cls='dropdown')