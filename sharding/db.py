from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Mapping of shard IDs to database connection URLs.
# Each shard represents a separate PostgreSQL database.
# In real systems, this helps scale writes and storage horizontally.
SHARD_DATABASES = {
    0: "postgresql://postgres:password@localhost/shard_0",
    1: "postgresql://postgres:password@localhost/shard_1",
    2: "postgresql://postgres:password@localhost/shard_2",
}

# Store SQLAlchemy Engine objects per shard
# Engines manage DB connections and connection pooling
engines = {}

# Store session factories per shard
# Each session factory is bound to a specific shard engine
sessions = {}

# Initialize an engine and session factory for each shard
for shard_id, db_url in SHARD_DATABASES.items():
    # Create a database engine for this shard
    engine = create_engine(db_url)

    # Save engine so it can be reused later
    engines[shard_id] = engine

    # Create a session factory bound to this shard's engine
    sessions[shard_id] = sessionmaker(bind=engine)

def get_session(shard_id: int):
    """
    Returns a new SQLAlchemy session connected to the specified shard.

    shard_id: Determines which database (shard) to route the request to.
    """
    return sessions[shard_id]()
