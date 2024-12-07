from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.db_config import Base
import sqlite3

db_file = "app.db"
sql_file = "utils/user.sql"

with sqlite3.connect(db_file) as conn:
    with open(sql_file, 'r') as f:
        sql_script = f.read()
    conn.executescript(sql_script)

print(f"Database initialized at {db_file}")

DATABASE_URL = 'sqlite:///app.db'
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)