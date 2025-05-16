from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str

class User(BaseModel):
    username: str
    password: str

class addUser(BaseModel):
    username: str
    password: str

class emoveUser(BaseModel):
    username: str
