from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from applepy.env import DATABASE_URL


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # important for MySQL timeouts
    pool_recycle=3600,  # avoids stale pooled connections
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
