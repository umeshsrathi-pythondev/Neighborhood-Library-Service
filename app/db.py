
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from app.config import settings

# attempt to connect to the configured database, fall back to sqlite file if unavailable
try:
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    # try a quick connection check
    conn = engine.connect()
    conn.close()
except OperationalError:
    # Postgres not running; use sqlite for development convenience
    sqlite_url = "sqlite:///./dev.db"
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
    settings.database_url = sqlite_url

# ensure tables exist (particularly useful for sqlite fallback)
from app import models  # import here to register metadata
models.Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
