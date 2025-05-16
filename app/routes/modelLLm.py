from fasthtml.common import *
from app.auth import Auth
from ..db.crud import ModelsCRUD
from ..models.database import get_db



modelcrud = ModelsCRUD(next(get_db()))
router = APIRouter(prefix="/models")


@router('/lrmodel', ['GET'])
def model(session,):    
    error, data = modelcrud.resultLR()
    return {'error': error, 'data': data}


@router('/rdgmodel', ['GET'])
def model(session,):
    error, data = modelcrud.resultRDG()
    return {'error': error, 'data': data}

@router('/kerasmodel', ['GET'])
def model(session,):
    error, data = modelcrud.resultKeras()
    return {'error': error, 'data': data}

@router('/kerasmodelM', ['GET'])
def model(session,):
    error, data = modelcrud.resultKerasM()
    return {'error': error, 'data': data}
