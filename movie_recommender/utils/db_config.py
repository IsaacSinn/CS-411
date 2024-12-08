# db_config.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_file = "app.db"
Base = declarative_base()

# Set up the SQLAlchemy engine and session
DATABASE_URL = f"sqlite:///{db_file}"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)  # Ensure tables are created from ORM models
Session = sessionmaker(bind=engine)