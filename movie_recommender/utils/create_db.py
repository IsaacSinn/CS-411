from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import Base

DATABASE_URL = 'sqlite:///example.db'
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)