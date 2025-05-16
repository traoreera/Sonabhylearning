from fasthtml.common import *
class BaseHtml:
    
    def __init__(self,
        body:Div = Div(),
        head:list = [],
        **kargv,
        ):
        self.body:list = body
        self.head:list = head
        self.kargv = kargv
        self.default()
        head = Head(*self.head)
        
        #body = Body(*self.body)
        self.html = Html(head, *body, **self.kargv)
    
    def render(self):
        return self.html
    
    
    def default(self):
        for i in [    
            Script(src='https://cdn.jsdelivr.net/npm/htmx.org@2.0.4/dist/htmx.min.js'),
            Script(src='https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js'),
            Script(src='https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js'),
            Script(src='https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js'),
        ]:
            self.head.append(i)
