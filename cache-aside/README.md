# Redis-based Cache_aside system

This project implements a cache-aside pattern for product data using multi-layer caching (Redis + in-memory hot cache) with PostgreSQL as the source of truth. Its goal is to reduce database load, speed up reads, and handle high traffic safely.

## Key Components

### 1. Hot Cache (LRU)

- An in-memory cache for the most frequently accessed products.

- Extremely fast access since it’s stored in the Node.js process memory.

- Example: If product id=1 is requested many times, it stays in memory for ultra-fast retrieval.

### 2. Redis Cache

- Distributed cache shared across multiple instances.

- Stores serialized product data and reduces database hits.

- Supports cache expiry to keep data fresh.

### 3. Database (PostgreSQL)

- Stores the authoritative product data.

- Used only on cache misses or for updates.

### 4. Cache Stampede Prevention

- Ensures multiple requests for the same uncached product don’t all hit the database at once.

- Achieved with a manual lock in Redis.

**Example:**\

- If 100 users request product id=1 at the same time, only one request fetches from the DB; the rest wait for the cache to be populated.

### 5. Metrics

- Prometheus counters track cache hits and cache misses.

- Helps understand cache efficiency under load.

## How It Works (Step-by-Step)

### 1. Request comes in for a product:

- First, check the hot in-memory cache.

- If not found, check the Redis cache.

- If still not found, try to acquire a Redis lock to prevent a cache stampede.

- If lock acquired, read from PostgreSQL, update Redis & hot cache, release the lock.

- If lock not acquired, wait a short time and retry reading from Redis.

### 2. Update product:

- Write changes to PostgreSQL.

- Immediately update Redis & hot cache to keep caches consistent (write-through).

- Background refresh worker (optional but recommended):

- Periodically refresh hot keys and cache entries to ensure popular items are always ready in memory.

## Execution workflow

### Step 0: Install Dependencies

- in terminal
  ```
  npm install express pg ioredis prom-client lru-cache dotenv
  ```
  ```
  npm install -D typescript ts-node @types/node @types/express k6
  ```

### Step 1: Set up PostgreSQL

- **Start PostgreSQL (local or Docker)**

  Local

  ```
  sudo service postgresql start
  ```

  OR Docker

  ```
  docker run --name postgres-cache -e POSTGRES_PASSWORD=password -e POSTGRES_USER=postgres -e POSTGRES_DB=cache_project -p 5432:5432 -d postgres
  ```

- **Create database & tables**

  If you don’t have products table yet:

  ```
  CREATE TABLE products (
     id SERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     price NUMERIC(10,2) NOT NULL,
     description TEXT
  );
  ```

### Step 2: Set up Redis

- Start Redis (standalone)

  ```
  docker run --name redis -p 6379:6379 -d redis
  ```

- Optional: Redis Cluster

  Example for 3-node cluster (requires ports 7000–7002)

  ```
  docker run -p 7000:7000 -p 7001:7001 -p 7002:7002 --name redis-cluster redis redis-server --cluster-enabled yes
  ```

### Step 3: Configure .env

- put this in the .env file
  ```
  DATABASE_URL=postgresql://postgres:password@localhost:5432/cache_project
  REDIS_URL=redis://localhost:6379
  REDIS_CLUSTER=false
  PORT=3000
  NODE_ENV=development
  ```

### Step 4: Run Express API

- Using ts-node (development)
  ```
  npx ts-node src/server.ts
  ```
  > Server should now be listening on port 3000.

### Step 5: Run Background Refresh Worker

- In a separate terminal
  ```
  npx ts-node src/background/refreshWorker.ts
  ```
  > This keeps hot keys and cache refreshed in the background.

### Step 7: Verify API

- GET product
  ```
  curl http://localhost:3000/products/1
  ```
- PUT update product price
  ```
  curl -X PUT -H "Content-Type: application/json" -d '{"price":99.99}' http://localhost:3000/products/1
  ```

### Step 8: Metrics (Prometheus)

- ```
  curl http://localhost:3000/metrics
  ```
  > Returns cache hits, cache misses, and other metrics.

### Step 9: Load Testing (k6)

- ```
  cd loadtest
  ```
- ```
  k6 run products.test.js
  ```

  > Simulates high concurrent traffic and shows how cache hit/miss behaves under load.

### Step 10: Monitor Redis

- ```
  redis-cli info
  ```
- ```
  redis-cli monitor
  ```
