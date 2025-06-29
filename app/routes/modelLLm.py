from fasthtml.common import *
from ..db.crud import ModelsCRUD
from ..models.database import get_db
from app.auth.Auth import token_validate_decorator

modelcrud = ModelsCRUD(next(get_db()))
router = APIRouter(prefix="/models")


@router('/lrmodel', ['GET'])
@token_validate_decorator
def model(session,):    
    error, data = modelcrud.resultLR()
    return {'error': error, 'data': data}


@router('/rdgmodel', ['GET'])
@token_validate_decorator
def model(session,):
    error, data = modelcrud.resultRDG()
    return {'error': error, 'data': data}

@router('/kerasmodel', ['GET'])
@token_validate_decorator
def model(session,):
    error, data = modelcrud.resultKeras()
    return {'error': error, 'data': data}

@router('/kerasmodelM', ['GET'])
@token_validate_decorator
def model(session,):
    error, data = modelcrud.resultKerasM()
    return {'error': error, 'data': data}
