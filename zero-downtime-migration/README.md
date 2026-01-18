# I built a backend project that demonstrates how to change a database schema in production without breaking the application or taking the system offline. The goal was to safely evolve the data model while real traffic could still be hitting the API.

## Zero-Downtime Migration: Order of Operations

- We follow the Expand → Migrate → Contract pattern.

# install dependencies

- npm install express sequelize pg dotenv && npm install -D typescript ts-node @types/express @types/node nodemon

## Step 1: Initial Setup (Baseline)

```
What happens

Database has only full_name

App only supports /v1/users

Traffic is live

Commands
npm install
npm run dev
```

## Step 2: EXPAND (Safe Schema Change)

```
What happens

Add new columns

No code breaks

Old API still works

Command
npm run migrate:add-columns


Equivalent to:

npx ts-node src/migrations/001_add_first_last_name.ts


DB now has:

full_name

first_name

last_name
```

## Step 3: MIGRATE (Backfill Existing Data)

```
What happens

Old rows updated in background

App remains online

No table locks

Command
npm run backfill


Equivalent to:

npx ts-node src/scripts/backfill_names.ts


All users now have:

first_name

last_name
```

## Step 4: Verify Migration Safety

```
What happens

Confirm no NULLs

Confirm v2 works

Confirm no code uses full_name anymore

Optional SQL check
SELECT COUNT(*) FROM users WHERE first_name IS NULL;


Expect:

0
```

### Step 5: CONTRACT (Remove Old Schema)

```
What happens

Remove legacy column

App already safe

Zero downtime

Command
npm run migrate:drop-column


Equivalent to:

npx ts-node src/migrations/002_drop_full_name.ts
```
