# database.py
# This file is responsible for setting up the database connection
# and providing shared objects used by the rest of the application.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database connection string
# Format:
# postgresql://<username>:<password>@<host>/<database_name>
DATABASE_URL = "postgresql://postgres:password@localhost/migration_demo"

# Create the SQLAlchemy engine
# The engine manages the actual connection to the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Create a session factory
# Each request or operation will create its own session
# Sessions are used to talk to the database (queries, inserts, updates, deletes)
SessionLocal = sessionmaker(bind=engine)

# Base class for all ORM models
# Every model class (User, Order, etc.) will inherit from this Base
# SQLAlchemy uses it to track tables and generate schema metadata
Base = declarative_base()
