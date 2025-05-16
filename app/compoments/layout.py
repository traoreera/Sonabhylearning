from fasthtml.common import *
from .controls import Controls


class Layout(Controls):

    def __init__(self):

        super(Layout, self).__init__()
        return

    def form(self, content, style, hx_target="#", hx_post="#", hx_trigger=''):
        return Form(*content, style=style, hx_post=hx_post, hx_target=hx_target, hx_trigger=hx_trigger)

    def title(self, title: str = "Home", *args, cls="container", style_file: str = "/css/style.css", **kwargs):
        return Link(rel="stylesheet", href=style_file), Favicon(light_icon="img/fastapi.png", dark_icon="img/fastapi.png"), Title(title), Main(*args, cls=cls, **kwargs)


layouts = Layout()