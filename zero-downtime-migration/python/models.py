# models.py
# Defines the User database model.
# This model is intentionally designed to support BOTH the old schema
# and the new schema at the same time to allow zero-downtime migrations.

from sqlalchemy import Column, Integer, String
from database import Base  # Shared Base class for all ORM models

class User(Base):
    # Name of the table in the database
    __tablename__ = "users"

    # Primary key column
    # Uniquely identifies each user record
    id = Column(Integer, primary_key=True)

    # -----------------------------
    # OLD SCHEMA COLUMN
    # -----------------------------
    # This column already exists in production.
    # It must remain available while older versions of the app are still running.
    # your Python code can use user.full_name, but in the DB the column remains fullName
    # fullName exists cos of a previous db design that is now conflicting with this schema even though it is empty
    full_name = Column("fullName", String, nullable=True)

    # -----------------------------
    # NEW SCHEMA COLUMNS
    # -----------------------------
    # These columns are added gradually in a safe migration.
    # They start as nullable so writes won't fail during rollout.
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    # Email field
    # Marked as NOT NULL because every user must have an email
    email = Column(String, nullable=False)
