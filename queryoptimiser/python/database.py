from sqlalchemy import create_engine           # Import function to create a DB engine
from sqlalchemy.orm import sessionmaker, declarative_base  # Import ORM session maker and base class for models

# URL for the database connection
# "sqlite:///./test.db" means:
# - Use SQLite
# - Store the database in the current folder as "test.db"
DATABASE_URL = "sqlite:///./test.db"

# Create the SQLAlchemy engine
# The engine manages the connection to the database
# `connect_args={"check_same_thread": False}` is required for SQLite
# so multiple threads (like FastAPI requests) can share the same connection
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a "SessionLocal" class
# This is a factory for session objects that will interact with the DB
# You use sessions to query, add, update, or delete rows
SessionLocal = sessionmaker(bind=engine)

# Base class for all ORM models
# Any class that represents a table in your database should inherit from this
Base = declarative_base()
