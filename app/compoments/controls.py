from fasthtml.common import *


class Controls:

    def __init__(self):

        super().__init__()
        return

    def input(self, ids='email', placeholder: str = 'email', autocomplete='email', required=True, tpe='email', style='',):

        return Input(type=tpe, id=ids, placeholder=placeholder, mame=ids, required=required, autocomplete=autocomplete, style="""""")

    def button(self, text="Submit", tps='submit', action="", onclick="", ids='button', style=""):
        return Button(text, type=tps, id=ids, name=ids, action=action, style=style)

    def h1(self, text):
        return H1(text)

    def h4(self, text): return H4(text)

    def toast(self, sesion, msg, type_msg):
        return add_toast(sesion, msg, type_msg)

    def link(self, text, text2):
        return H5(text, A(text2, href=text2))

    def label(self, text="Submit", tps='', fr='username', style=''):

        return Label(text, fr=fr, style=style)

    def img(self, src='img/fastapi.png', alt="fastapi"):
        return Img(src=src, alt=alt)

    def script_chart(self,):

        return Script(src="https://cdn.jsdelivr.net/npm/chart.js")

    def my_script(self, script: str = '/js/script.js'):

        return Script(src=script)

    def head_cloudFare(self):

        return Head(Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"))