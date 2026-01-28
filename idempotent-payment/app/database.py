from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection string:
# - Uses PostgreSQL as the database
# - Connects to the `payments_db` database
# - Credentials and host are defined here (typically moved to env vars in production)
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/payments_db"

# Create the SQLAlchemy engine
# - Manages the connection pool to the database
# - Reuses connections efficiently instead of opening a new one per request
engine = create_engine(DATABASE_URL)

# Create a session factory
# - Each session represents a single database transaction scope
# - Sessions are created per request and closed after use
SessionLocal = sessionmaker(bind=engine)
