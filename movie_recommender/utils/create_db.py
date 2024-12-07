import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.db_config import Base
import sqlite3
from utils.logger import configure_logger
import logging

# Paths to database and SQL file
db_file = "app.db"
sql_file = "utils/user.sql"

# Configure logging
logger = logging.getLogger(__name__)
configure_logger(logger)

# Check if the database file exists
if os.path.exists(db_file):
    os.remove(db_file)  # Delete the existing database file
    print(f"Deleted existing database at {db_file}")

# Create the new database and initialize the schema
with sqlite3.connect(db_file) as conn:
    with open(sql_file, 'r') as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    print(f"Database initialized at {db_file}")

# Set up the SQLAlchemy engine and session
DATABASE_URL = f"sqlite:///{db_file}"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)  # Ensure tables are created from ORM models
Session = sessionmaker(bind=engine)

# Log database setup completion
logger.info("Database setup complete.")