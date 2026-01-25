# Wallet Service (Double-Spend / Race Condition Demo)

## What the project is

This project is a simulated wallet service that stores user balances and allows withdrawals. It demonstrates how race conditions can break real-world financial systems and shows how to fix them with proper database transactions.

## Problem it solves

Imagine two users try to withdraw money at the same time from the same wallet:

- Without safeguards: both requests can succeed, leaving the wallet in a negative balance — a classic double-spend problem.

- With safeguards: one request succeeds, the other fails, ensuring data integrity.

This is a common real-world problem in banking, payment systems, and any app dealing with money.

## How it works

1. Database: PostgreSQL stores wallets and balances.

2. API: Node.js + Express endpoints:
   - /withdraw/unsafe: demonstrates what happens without protection

   - /withdraw/safe: uses transactions and row-level locks to prevent double spending

3. Concurrency simulation: You can send two requests at the same time to see the race condition happen.

4. Verification: Check balances in the database to confirm correctness.

## Full Execution Flow (Local Postgres)

### Install dependencies

```
npm install express pg dotenv
```

```
npm install -D typescript ts-node @types/node @types/express
```

### 1 Start PostgreSQL locally

- Make sure Postgres is running:

  ```
  sudo service postgresql start
  ```

- Check status:

```
sudo service postgresql status
```

### 2 Create the database user and database

- Switch to the Postgres user:

  ```
  sudo -u postgres psql
  ```

- Inside the psql shell:

  ```
  -- Create the wallet user
  CREATE USER wallet WITH PASSWORD 'wallet';

  -- Create the database
  CREATE DATABASE wallet_db OWNER wallet;

  -- Grant privileges
  GRANT ALL PRIVILEGES ON DATABASE wallet_db TO wallet;

  -- Exit
  \q
  ```

### 3 Apply the database schema

Assuming your `sql/schema.sql` exists:

```
psql postgres://wallet:wallet@localhost:5432/wallet_db -f sql/schema.sql
```

This will create:

- wallets table

### 4 Start the API server

```
npx ts-node src/server.ts
```

- Expected output:

```
Wallet service running on port 3000
```

### 5 Test endpoints

- Unsafe endpoint (simulate race condition):
  Open two terminals and run simultaneously:

  ```
   curl -X POST localhost:3000/withdraw/unsafe \
   -H "Content-Type: application/json" \
   -d '{"amount": 60000}'
  ```

  > Expected: Both succeed → balance can go negative

- Safe endpoint (transactional fix):

  ```
  curl -X POST localhost:3000/withdraw/safe \
  -H "Content-Type: application/json" \
  -d '{"amount": 60000}'
  ```

  > Expected: One succeeds, one fails → balance stays correct
