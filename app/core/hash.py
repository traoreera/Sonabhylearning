from passlib.context import CryptContext
from app.settings.config import HashConfiguration


pwd_cxt = CryptContext(schemes=['bcrypt'], )#deprecated=HashConfiguration.DEPRECATED)


class Hash():
    
    @staticmethod
    def bcrypt(password: str) -> str:
        return pwd_cxt.hash(password)
    
    @staticmethod
    def verify(hashed_password, plain_password) -> bool:
        return pwd_cxt.verify(plain_password, hashed_password)