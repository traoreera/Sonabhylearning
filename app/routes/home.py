from fasthtml.common import *
from app.auth import Auth
from ..db.crud import UsersCRUD
from ..models.database import get_db
from ..pages.home import DashBord

bord = DashBord()   

router = APIRouter(prefix="/dashbord")

@router('/', ['GET'])
#@Auth.token_validate_decorator
def dashbord(session,):
    return bord.page()