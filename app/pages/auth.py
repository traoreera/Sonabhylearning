
from app.compoments import Layout, Controls
from .css import login_
from fasthtml.common import *


class LoginPages(Layout, Controls):

    def __init__(self):
        super().__init__()
        return

    def content(self):
        return [
            self.img(),
            self.h4(text='Admin'),
            self.input(ids='username', placeholder='email or username',autocomplete='email', required=True, tpe=''),
            self.input(ids='password', placeholder='password',autocomplete='current-password', required=True, tpe='password',),
            self.button(text="Submit", tps='submit', action="",
                        onclick="", ids='button', style=login_.BUTTON_STYLE),
            self.link("do not have acount?", " register")
        ]

    def loginForm(self):
        return self.form(
            content=self.content(),
            hx_target="#response",
            hx_post="/auth/login",
            style=login_.FORM_STYLE
        )

    def page(self):

        return Html(
            Head(
                Meta(charset='UTF-8'),
                Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
                Link(rel="stylesheet", href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css'),
                Link(rel="stylesheet", href='/css/index.css'),
                Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
                Script(src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js'),
                Script(src='https://cdn.jsdelivr.net/npm/htmx.org@2.0.4/dist/htmx.min.js'),
                Script(src='https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js'),
                Script(src='https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js'),
                Script(src='https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js'),
            ),
            Body(
                Div(self.loginForm(), style=login_.DIV_STYLE), Span(id='response'),
            )
        )









class AddUser(Layout, Controls):

    def __init__(self):
        super().__init__()
        return

    def controls(
        self,
        ids: str = "email",
        placeholder: str = 'email',
        autocomplete='email',
        required=True,
        tpe='email',
    ):

        return [
            self.label(
                text=ids,
                tps='',
                fr='',
                style=''
            ),
            self.input(ids=ids, placeholder=placeholder,
                       autocomplete=autocomplete, required=required, tpe=tpe,)
        ]

    def content(self):
        return [
            H1("New user"),
            Input(type='email', id='email', name='email',required='', placeholder='Entrez votre email'),
            Input(type='password', id='password', name='password',required='', placeholder='Entrez votre mot de passe'),P('', id='strength-bar'),
            Input(type='password', id='confirm_password', name='confirm_password',required='', placeholder='Confirmez votre mot de passe'),
            P(id='password-match-message'),
            Button('Créer le compte', type='submit', cls='contrast',sytle=login_.BUTTON_STYLE, id='submit-button')
        ]

    def page(self):
        form = self.form(
            content=self.content(),
            hx_post='#',
            hx_target='#response',
            style=login_.FORM_STYLE
        )
        return self.title(
            "Create User",
            Section(
                form,
                Script(src='/js/user.js'), 
                cls='container',
                id='response',
                style=login_.DIV_STYLE,
                title="Create User"
                )
        )



login_pages = LoginPages()
add_user = AddUser()