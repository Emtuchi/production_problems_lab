-- =========================
-- Wallets table
-- Stores the current balance for each user.
-- One wallet per user is enforced to prevent duplicates.
-- =========================
CREATE TABLE IF NOT EXISTS wallets (
    id SERIAL PRIMARY KEY,            -- Internal unique identifier for the wallet
    user_id INTEGER UNIQUE NOT NULL,  -- Each user can have only one wallet
    balance NUMERIC NOT NULL DEFAULT 0 -- Current wallet balance (cannot be NULL)
);

-- =========================
-- Payments table
-- Records every payment attempt.
-- Uses an idempotency key to prevent duplicate charges
-- when the same request is retried.
-- =========================
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,                -- Unique payment record ID
    user_id INTEGER NOT NULL,             -- User making the payment
    amount NUMERIC NOT NULL,              -- Amount of money involved in the payment
    idempotency_key TEXT NOT NULL UNIQUE, -- Ensures the same payment is processed only once
    status TEXT NOT NULL,                 -- Payment state (e.g. 'pending', 'success', 'failed')
    created_at TIMESTAMP DEFAULT now()    -- Timestamp for auditing and debugging
);
