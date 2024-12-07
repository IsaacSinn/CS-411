from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import Base
import sqlite3

db = "example.db"
sql_file = "user.sql"

with sqlite3.connect(db_file) as conn:
    with open(sql_file, 'r') as f:
        sql_script = f.read()
    conn.executescript(sql_script)

print(f"Database initialized at {db}")

DATABASE_URL = 'sqlite:///example.db'
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)