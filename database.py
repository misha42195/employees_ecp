
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine, AsyncSession
)
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(settings.DB_URL)
async_session_maker = async_sessionmaker(engine,expire_on_commit=False)



class Base(DeclarativeBase):
    pass
