from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Base class that all SQLAlchemy models will inherit from.
# It keeps track of table definitions and metadata.
Base = declarative_base()

class User(Base):
    # Name of the table in the database
    __tablename__ = "users"

    # Primary key column
    # - Integer: data type
    # - primary_key=True: uniquely identifies each row
    id = Column(Integer, primary_key=True)

    # User's name
    # - String: variable-length text
    # - nullable=False: this field is required and cannot be NULL
    name = Column(String, nullable=False)

    # User's email address
    # - unique=True: enforces uniqueness at the database level
    #   (prevents two users from having the same email)
    email = Column(String, unique=True)
