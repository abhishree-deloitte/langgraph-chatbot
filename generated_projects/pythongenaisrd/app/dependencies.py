from sqlalchemy.orm import Session
from app.db import get_db_session

async def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()