from fasthtml.common import *
from app.routes import AuthRoute
from app.routes import home
from app.routes import modelLLm
#from task.runTask import task
from app.pages.home import Index, license, explain, ia


app, rt = fast_app(live=True, debug=True,static_path='./static')

AuthRoute.router.to_app(app)
home.router.to_app(app)
modelLLm.router.to_app(app)


@rt('/', ['GET'])
def index():
    return Index()



@rt('/LICENCE', ['GET'])
def licence():
    return license()

@rt("/explain")
def explainDocs():
    return explain()

@rt('/ia')
def iaDocs():
    return ia()

#create 404 not found page
@app.on_event("startup")
async def startup_event():
    pass
    #task.scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    pass
    #task.scheduler.shutdown()
if __name__ == "__main__":
    
    serve(host="0.0.0.0", port=5000,)   