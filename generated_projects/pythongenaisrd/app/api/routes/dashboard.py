from fastapi import APIRouter
from app.database import SessionLocal
from app.database.models import User
from app.schemas import DashboardTile

router = APIRouter()

@router.get("/tiles")
def get_dashboard_tiles():
    db = SessionLocal()
    users = db.query(User).all()
    tiles = []
    for user in users:
        tile = DashboardTile(
            id=user.id,
            name=user.name,
            email=user.email,
        )
        tiles.append(tile)
    return tiles