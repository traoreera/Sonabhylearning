from datetime import datetime
import uuid
from app.models.database import Base
from datetime import timedelta
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, Boolean
from app.core.hash import Hash
from app.settings.config import TokenConfiguration 

class AdminBase(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=Flase)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, username, password):
        self.email = username
        self.password = password
    
    def responseModel(self):
        return{
            "email": self.email,
            "created_at": self.created_at
        }
    
    def verify_password(self, password):
        return Hash.verify(self.password, password)


class UserSession(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, unique=True)
    user_id = Column(String, unique=True, nullable=False)
    
    session_key = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    expirate_at = Column(TIMESTAMP,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    def __init__(self,user_id: str, token:str, ):
        
        self.id = str(uuid.uuid4())[:30]
        self.user_id = user_id
        self.session_key = token
        self.created_at = datetime.utcnow()
        self.expirate_at = datetime.utcnow() + timedelta(minutes=TokenConfiguration.ACCESS_TOKEN_EXPIRE_MINUTES)
        
