from pydantic import BaseModel

class LoginCredentials(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str
    role: str