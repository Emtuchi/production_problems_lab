# scripts/backfill_names.py
# Backfills data into newly added columns without downtime
# This runs AFTER the schema expansion and while the app is live.

from database import SessionLocal
from models import User

# Create a database session
db = SessionLocal()

# Select only users that have NOT been backfilled yet
# This makes the script:
# - Safe to rerun
# - Incremental
# - Non-destructive

users = db.query(User).filter(User.first_name.is_(None)).all()

for user in users:
    # Skip users that do not have the old full_name field populated
    # (avoids corrupt or partial data)
    if not user.full_name:
        continue

    # Split the old full_name into first and last names
    # This is a simple heuristic for demo purposes
    parts = user.full_name.split(" ")
    user.first_name = parts[0]
    user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

    # Mark the row as updated
    db.add(user)

# Commit all updates in a single transaction
# This avoids partial writes and keeps the operation atomic
db.commit()

# Confirmation log
print("✅ Backfill completed")
