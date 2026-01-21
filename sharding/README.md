# Sharding Logic Simulator

This project demonstrates application-level database sharding.

## What it shows

- How shard routing works
- Why shard keys matter
- How hot shards form
- Why resharding is expensive

## Key Insight

Changing the number of shards causes massive data movement when using modulo-based sharding so we use consistent hashing.

## Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy

## Sharding Project Overview

```
The goal of this part of the project is to simulate and implement database sharding: distributing your data across multiple database instances to improve performance, scalability, and fault tolerance.

Sharding is important when a single database becomes too large or too slow to handle all traffic.
```

### Key Components

#### 1. Shard Setup

```
Multiple PostgreSQL databases represent shards, e.g. shard_0, shard_1, shard_2.

Each shard has its own SQLAlchemy engine and session.

Example:

SHARD_DATABASES = {
    0: "postgresql://.../shard_0",
    1: "postgresql://.../shard_1",
    2: "postgresql://.../shard_2",
}

This allows the app to read/write to the correct shard.
```

#### 2. User Routing

```
Each user is assigned to a shard using a shard ID calculation:

Naive modulo method: shard_id = user_id % number_of_shards

Consistent hashing: maps user IDs to shards in a way that minimizes data movement if shards are added or removed.

This ensures that each user always goes to the same shard.
```

#### 3. Data Models

```
Each shard contains the same table structure (User table).

Data is physically split, but the app logically treats all shards as one dataset.
```

#### 4. Shard Health Management

```
ShardHealthRegistry tracks which shards are healthy.

Failed shards can be marked down and the hash ring is rebuilt to route traffic only to healthy shards.

Failed shards can be restored and traffic is rebalanced.
```

#### 5. Consistent Hashing

```
Naive modulo sharding is simple but problematic when adding new shards (most data needs to move).

Consistent hashing solves this:

Only a small portion of users move to new shards when the number of shards changes.

Uses virtual nodes for smooth load distribution.
```

#### 6. Scripts & Demo

- Step 1

```
# Create databases for shards

psql -U postgres -c "CREATE DATABASE shard_0;"
psql -U postgres -c "CREATE DATABASE shard_1;"
psql -U postgres -c "CREATE DATABASE shard_2;"

# Activate your virtual environment

- python3 -m venv venv
- source venv/bin/activate

# Install dependencies

- pip install fastapi uvicorn sqlalchemy psycopg2-binary faker

```

- Step 2 - This ensures users table exists on all shard databases

```
python3 -c "from app import engines, Base; [Base.metadata.create_all(bind=e) for e in engines.values()]"
```

- Step 3 - Seed shards with fake users

```
- python3 -m scripts.seed_users
```

- Step 4 - Start FastAPI application

```
uvicorn app:app --reload
```

- Step 5 - Verify shard distribution

```
curl http://127.0.0.1:8000/shards/status
```

- Step 6 - Simulate rebalancing

```
python3 -m scripts.rebalance
```

- step 7 - Simulate shard failure

```
python3 -m scripts.simulate_failure
```

- Step 7 - Simulate hot key traffic

```
python3 -m scripts.hot_key_simulation
```

- Step 8 - Add or remove shards

```
# Example in Python shell

from shard_router import mark_shard_down, mark_shard_up

mark_shard_down(2)  # take shard 2 offline

mark_shard_up(2)    # bring it back
```

#### 7. Benefits

```
- Allows the database to scale horizontally.

- Handles large datasets efficiently.

- Supports high availability by routing around failed shards.

- Demonstrates modern production strategies for sharded databases.
```
