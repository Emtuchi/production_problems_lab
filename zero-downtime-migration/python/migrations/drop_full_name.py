# migrations/drop_full_name.py
# Final cleanup migration
# This runs ONLY after:
# 1) New columns (first_name, last_name) exist
# 2) All data has been backfilled
# 3) All application code no longer reads or writes full_name

from database import engine
from sqlalchemy import text

# Open a direct database connection
# Using raw SQL here avoids ORM coupling during destructive changes
with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE users
        DROP COLUMN IF EXISTS full_name;
    """))
    conn.commit()

# Log success for visibility in deployment pipelines
print("✅ full_name column dropped")
