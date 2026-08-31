from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres.ainvamrqpmkxfjhsvuch:ExpeseTracker@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgresr"

engine = create_engine(SQLALCHEMY_DATABASE_URL,)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()