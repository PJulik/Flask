import os
import atexit

from sqlalchemy import Column, Integer, Text, create_engine, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = os.getenv('POSTGRES_USER', 'app')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'app')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)
atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

class Ad(Base):
    __tablename__ = 'app_ad'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False, index=True)
    owner = Column(String(100), nullable=False, index=True)
    creation_date = Column(DateTime, server_default=func.now())

Base.metadata.create_all()