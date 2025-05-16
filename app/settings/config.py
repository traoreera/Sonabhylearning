import os

class TokenConfiguration:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")


class HashConfiguration:
    SCHEME = [os.environ.get("SCHEME")]
    DEPRECATED = os.environ.get("DEPRECATED")