from sqlalchemy.orm import Session
from app.database import get_db

def get_db():
    db = get_db()
    try:
        yield db
    finally:
        db.close()