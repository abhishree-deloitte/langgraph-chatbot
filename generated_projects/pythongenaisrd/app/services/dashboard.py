from sqlalchemy.orm import Session
from app.db.models import User

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_tiles(self):
        # implement dashboard tile logic here
        # for demonstration purposes, return a dummy response
        return {"tiles": [{"id": 1, "name": "Tile 1"}, {"id": 2, "name": "Tile 2"}]}