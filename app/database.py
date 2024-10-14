import os

import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

# Path to the SQLite database
db_path = "./database.db"

# Check if the database file exists and remove it
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"{db_path} has been deleted.")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = _sql.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()
Base.metadata.create_all(bind=engine)
