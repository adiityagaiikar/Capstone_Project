import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/roadsafety")

try:
    # Safely test the connection
    test_engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with test_engine.connect() as conn:
        print("Successfully connected to PostgreSQL database.")
    engine = test_engine
except Exception as e:
    print(f"Failed to connect to PostgreSQL: {e}")
    print("Falling back to SQLite database for immediate execution.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
