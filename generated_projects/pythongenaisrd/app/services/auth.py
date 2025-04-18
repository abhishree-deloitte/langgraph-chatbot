from sqlalchemy.orm import Session
from app.db.models import User

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, data: LoginSchema):
        # implement login logic here
        # for demonstration purposes, return a dummy response
        return {"access_token": "dummy_token", "user_id": 1}