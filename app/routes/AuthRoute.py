from fasthtml.common import *
from app.auth import Auth
from ..pages.auth import login_pages, add_user
from ..db.crud import UsersCRUD
from ..models.database import get_db
from ..models.admin import AdminBase

userCrud = UsersCRUD(next(get_db()))
router = APIRouter(prefix="/auth")


@router(path="/",methods=["GET"])
@router(path="/login",methods=["GET"])
def Login(session):
    if session.get('token'):
        response = userCrud.validation(session['token'])
        if response == True:
            return Redirect('/')
    return login_pages.page()


@router(path="/login",methods=["POST"])
def LoginPost(session, username:str, password: str):
    response, token = Auth.login(session, username, password)
    if response == True:
        return Redirect('/')
    else:
        return Redirect('/auth/login')



@router(path="/register",methods=["GET"])
def register(session):
    return add_user.page()

@router(path="/register",methods=["POST"])
def registerPost(session, email:str, password: str):
    response =userCrud.add(
        admin= AdminBase(username=email,password=password)
    )
    if response:
        return Redirect('/login')



@router(path="/logout",methods=["GET"])
@Auth.token_validate_decorator
def logout(session):
    Auth.logout(session)
    return Redirect('/auth')



