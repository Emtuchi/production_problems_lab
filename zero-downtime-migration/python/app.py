# app.py
# Entry point for the FastAPI application.
# This file wires together database setup and multiple API versions
# to support zero-downtime schema migration.

from fastapi import FastAPI
from database import engine
from models import Base
from routes import v1_users, v2_users

# Create the FastAPI application instance
app = FastAPI()

# Create database tables if they do not exist.
# This is acceptable for demos and local development.
# In real production systems, schema changes should be handled
# via controlled migration scripts instead of create_all().
Base.metadata.create_all(bind=engine)

# Mount version 1 of the API (legacy clients).
# These endpoints continue to use the old schema (full_name).
app.include_router(v1_users.router, prefix="/v1")

# Mount version 2 of the API (new clients).
# These endpoints use the new schema (first_name / last_name)
# while maintaining compatibility through dual writes.
app.include_router(v2_users.router, prefix="/v2")
