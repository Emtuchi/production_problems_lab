# migrations/add_first_last_name.py
# Database migration: safe schema expansion (non-breaking change)
# This migration adds new columns without affecting existing code or data.

from sqlalchemy import text
from database import engine

# Open a direct database connection using the SQLAlchemy engine
with engine.connect() as conn:
    # ALTER TABLE is used to evolve the schema in place.
    # ADD COLUMN IF NOT EXISTS ensures:
    # - The migration is idempotent (safe to run multiple times)
    # - Existing deployments do not break if the column already exists
    #
    # Adding nullable columns is a zero-downtime operation in PostgreSQL
    # because it does not rewrite the table or lock it for long periods.
    # In 2.0, raw SQL must be wrapped using text().
    conn.execute(text("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS first_name TEXT,
        ADD COLUMN IF NOT EXISTS last_name TEXT;
    """))
    conn.commit()

# Log confirmation that the migration completed successfully
print("✅ first_name and last_name columns added")
