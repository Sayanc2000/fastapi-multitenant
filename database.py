import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema

load_dotenv()

db_host = os.environ.get("POSTGRES_HOST")
db_user = os.environ.get("POSTGRES_USER")
db_password = os.environ.get("POSTGRES_PASSWORD")
db_name = os.environ.get("POSTGRES_DB")
db_port = os.environ.get("POSTGRES_PORT", 5432)  # Default to 5432 if not set

# Construct the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_schema_if_not_exists(schema_name):
    with engine.connect() as conn:
        conn.execute(CreateSchema(schema_name, if_not_exists=True))
        conn.commit()


def get_base(tenant_name: str):
    create_schema_if_not_exists(tenant_name)
    metadata = MetaData(schema=tenant_name)
    Base = declarative_base(metadata=metadata)
    return Base


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
