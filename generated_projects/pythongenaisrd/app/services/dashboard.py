from sqlalchemy.orm import Session
from app.db.models import User

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_tiles(self):
        # implement dashboard tile logic
        pass