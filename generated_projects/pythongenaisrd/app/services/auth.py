from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.auth import LoginCredentials, User

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, credentials: LoginCredentials):
        # implement login logic
        pass

    def get_current_user_details(self):
        # implement current user details logic
        pass