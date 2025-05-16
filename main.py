from fasthtml.common import *
from app.routes import AuthRoute
from app.routes import home
from app.routes import modelLLm

app, rt = fast_app(live=True, debug=True,static_path='./static')

AuthRoute.router.to_app(app)
home.router.to_app(app)
modelLLm.router.to_app(app)



if __name__ == "__main__":
    
    serve(host="0.0.0.0", port=5000,)   