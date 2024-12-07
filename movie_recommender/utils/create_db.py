import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.db_config import Base
import sqlite3
from utils.logger import configure_logger
import logging

db_file = "app.db"
sql_file = "utils/user.sql"

logger = logging.getLogger(__name__)
configure_logger(logger)

# Check if the database file exists
if not os.path.exists(db_file):
    # If the database does not exist, create it and initialize the schema
    with sqlite3.connect(db_file) as conn:
        with open(sql_file, 'r') as f:
            sql_script = f.read()
        conn.executescript(sql_script)

    logger.info(f"Database initialized at {db_file}")
else:
    logger.info(f"Database already exists at {db_file}")

# Set up the SQLAlchemy engine and session
DATABASE_URL = f"sqlite:///{db_file}"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)  # This ensures that the tables are created if not present
Session = sessionmaker(bind=engine)