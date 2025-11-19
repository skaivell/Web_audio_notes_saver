from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr
from app.config import get_db_url

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = get_db_url()
#engine = create_async_engine(DATABASE_URL, echo= True)
#new_async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

engine = create_engine(DATABASE_URL)
sesson_local = sessionmaker(autoflush=False, autocommit= False, bind=engine)

Base = declarative_base()

#class Base(AsyncAttrs, DeclarativeBase):
#    __abstract__ = True
#
#    @declared_attr.directive
#    def __tablename__(cls) -> str:
#        return f"{cls.__name__.lower()}s"