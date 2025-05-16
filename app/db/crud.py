from datetime import datetime
from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.admin import AdminBase, UserSession
from app.models.result import RGDResult,KerasResultMulti, KerasResultSimple, ResulttLineareRegretion
from app.db.schemas import Login
from app.auth.token import verify_token, create_access_token

class UsersCRUD:
    def __init__(self, session:Session):
        self.session = session

    def add(self, admin:AdminBase):
        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)
        return admin
    
    def get_by_username(self, username):
        return self.session.query(AdminBase).filter(AdminBase.username == username).first().responseModel()
    
    def remove(self, admin:AdminBase):
        self.session.delete(admin)
        self.session.commit()

    def get_all(self):
        return self.session.query(AdminBase).all()

    def login(self, login_credentials: Login) -> dict:
        """
        Méthode pour se connecter à un utilisateur.

        Args:
            login_credentials (Login): Les informations de connexion de l'utilisateur.

        Returns:
            dict: Un dictionnaire contenant le token de connexion et un message de réussite ou d'échec.

        Raises:
            HTTPException: Si les informations de connexion sont incorrectes.
        """
        user = self.session.query(AdminBase).filter(AdminBase.email == login_credentials.email).first()

        if not user:
            return {'message': 'user not found'}
        if user.verify_password(login_credentials.password):
            # verified if user as token on database
            session = self.session.query(UserSession).filter(
                (UserSession.user_id == user.id) | (UserSession.expirate_at > datetime.utcnow())
            ).first()
            token = create_access_token({"email": user.email})

            if not session:
                session = UserSession(user_id=user.id, token=token)
                self.session.add(session)
                self.session.commit()
                self.session.refresh(session)
                return {'token': token, 'message': 'login successful'}
            else:
                current_user = self.get_user(session.session_key)
                if current_user:
                    token = create_access_token({"email": user.email})
                    session.session_key = token
                    self.session.commit()
                    self.session.refresh(session)
                    return {'token': token, 'message': 'login successful'}
                else:
                    return {'message': 'user not found'}
        else:
            return {'message': 'wrong password or not found user with this id'}

    def get_user(self, token: str) -> AdminBase:
            try:
                payload = verify_token(token, HTTPException(
                    status_code="401",
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                ))
                user = self.session.query(AdminBase).filter(AdminBase.email == payload.email).first()
                if user:
                    return user
                else:
                    return None
            except Exception as e:
                # log the error or return a meaningful error message
                return None

    def validation(self, token: str):
        
        response = self.get_user(token)
        if response:
            return True
        else:
            return False
        


class ModelsCRUD:
    def __init__(self, session:Session):
        self.session = session
    
    
    def resultRDG(self,):
        response = self.session.query(RGDResult).all()
        errorRGD = [f'{i.predicted_error:.1f}' for i in response ]
        dataRGD = [i.predicted_date for i in response ]
        return errorRGD, dataRGD
    
    def resultLR(self,):
        response = self.session.query(ResulttLineareRegretion).all()
        errorLR = [f'{i.predicted_error:.1f}' for i in response]
        dataLR = [i.predicted_date for i in response]
        return errorLR, dataLR
    
    def resultKeras(self,):
        response = self.session.query(KerasResultSimple).all()
        
        errorSGD = [f'{i.predicted_error:.1f}' for i in response]
        dataSGD = [i.predicted_date for i in response]
        
        return errorSGD, dataSGD
    
    def resultKerasM(self,):
        response = self.session.query(KerasResultMulti).all()
        
        error =[f'{i.predicted_error:.1f}' for i in response ]
        dataM = [i.predicted_date for i in response]
        
        return error, dataM