# Zero-Downtime Migrations Project

## Goal

```
The project demonstrates how to change a database schema safely in production without taking the system offline or breaking the application.

Many applications face the challenge of evolving their database while real users are still interacting with the system. This project simulates a strategy to add, backfill, and remove columns safely, ensuring continuous operation.
```

## Key Concepts

### 1. Dual-Write / Backward Compatibility

```
Old columns remain available for the existing API.

New columns are added without removing old ones, so both old and new APIs can work at the same time.

Example:

Old column: fullName

New columns: first_name, last_name

Both old and new columns are written to simultaneously.

Safe Schema Changes

Use ALTER TABLE … ADD COLUMN IF NOT EXISTS to add new columns without breaking the table.

Avoid dropping old columns until all code paths and data backfills are verified.
```

### 2. Backfilling Data

```
After adding new columns, existing data is copied from the old column to the new columns.

Example:

fullName → split into first_name and last_name

Done via a script that updates rows in batches to avoid locking the table.

Final Cleanup

Once all code and clients are using the new schema:

Old columns (e.g., fullName) are dropped safely.

This ensures the database stays clean and the new schema is fully adopted.
```

### 3. Incremental Deployment

```
Code changes are deployed before the schema is fully switched.

Allows dual reading/writing, making it possible to roll back safely if something goes wrong.
```

### 4. Zero-Downtime Migration Steps for a simple name change on a database(postgresql)

1. Add Columns

```
Add first_name and last_name using ALTER TABLE IF NOT EXISTS.

Table remains available for reading and writing.
```

2. Deploy Dual-Write Code

```
API writes to both old and new columns simultaneously.

Old API continues working for existing clients.
```

3. Backfill Data

```
Script copies existing fullName values into first_name and last_name.

Can be run without downtime.
```

4. Switch APIs

```
Existing clients can migrate to the new API (v2).

Old API can eventually be deprecated.
```

5. Drop Old Columns

```
Once verified, safely remove fullName.
```

### Why This Matters

```
Avoids service downtime when evolving the database schema.

Enables incremental deployment and safe migration in production environments.

Demonstrates best practices used in large-scale production systems.
```
