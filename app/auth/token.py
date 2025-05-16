from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.db import schemas
from app.settings.config import TokenConfiguration


def create_access_token(data: dict):
    to_encode: dict = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TokenConfiguration.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        TokenConfiguration.SECRET_KEY,
        algorithm=TokenConfiguration.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, TokenConfiguration.SECRET_KEY, algorithms=[
                TokenConfiguration.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception