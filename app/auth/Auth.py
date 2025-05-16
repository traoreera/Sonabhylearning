from fasthtml.common import *
from functools import wraps
from app.models import database
from app.db.crud import UsersCRUD
from app.db.schemas import Login

user_validation = UsersCRUD(next(database.get_db()))

def token_validate_decorator(f):
    """
    Décorateur qui vérifie la présence et la validité d'un token dans la session
    avant d'appeler la fonction décorée.

    :param f: La fonction à décorer
    :return: La fonction décorée
    """
    @wraps(f)
    def wrapper(session, *args, **kwargs):
        if session is None or "token" not in session:
            return Redirect('/auth/')
        token = session["token"]
        if not isinstance(token, str) or token.strip() == "":
            del session["token"]
            return Redirect('/auth/')
        try:
            response = user_validation.validation(token=session['token'])
            if response is False:
                return Redirect('/auth')
            return f(session, *args, **kwargs)
        except Exception as e:
            del session["token"]
            return Redirect('/auth/login')
    return wrapper


def login(session,usernme,password):    
    Login.email = usernme
    Login.password = password
    user_token = user_validation.login(Login)
    if user_token['message'] == 'login successful':
        session['token'] = user_token['token']
        return (True,user_token['token'])
    else:
        return (False,user_token['message'])




@token_validate_decorator
def logout(session):
    if 'token' in session:
        del session['token']
        return True
    else:
        return False