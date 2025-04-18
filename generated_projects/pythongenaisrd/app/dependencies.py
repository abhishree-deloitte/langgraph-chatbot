from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import DATABASE_URL

async def get_db_session():
    engine = create_async_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine, class_=AsyncSession)
    session = Session()
    try:
        yield session
    finally:
        await session.close()