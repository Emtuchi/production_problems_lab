-- Create a wallets table to store user balances
CREATE TABLE wallets (
  id SERIAL PRIMARY KEY,              -- Auto-incrementing unique wallet ID
  user_id INT UNIQUE NOT NULL,         -- Each user can only have one wallet (1-to-1 relationship)
  balance BIGINT NOT NULL CHECK (balance >= 0), 
                                      -- Wallet balance stored as integer (e.g. kobo/cents)
                                      -- CHECK ensures balance can never go negative
  updated_at TIMESTAMP DEFAULT NOW()   -- Timestamp for last update (auto-filled on insert)
);

-- Seed the table with a sample wallet record
INSERT INTO wallets (user_id, balance)
VALUES (1, 10000); -- Initial balance = ₦10,000 (stored in lowest currency unit)
