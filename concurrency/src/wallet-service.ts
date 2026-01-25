import { pool } from "./db";

export async function withdrawSafe(userId: number, amount: number) {
  // Acquire a client connection from the PostgreSQL pool
  // This allows multiple queries to run in the same transaction
  const client = await pool.connect();

  try {
    // Start a database transaction
    // Ensures all subsequent operations are atomic (all succeed or all fail)
    await client.query("BEGIN");

    // Lock the user's row for update to prevent race conditions
    // FOR UPDATE ensures no other transaction can modify this row until we finish
    const res = await client.query(
      "SELECT balance FROM wallets WHERE user_id = $1 FOR UPDATE",
      [userId]
    );

    const balance = res.rows[0].balance;

    // Check if the user has sufficient balance
    if (balance < amount) {
      // Throwing an error will trigger rollback
      throw new Error("Insufficient funds");
    }

    // Deduct the amount from the user's balance
    await client.query(
      "UPDATE wallets SET balance = balance - $1 WHERE user_id = $2",
      [amount, userId]
    );

    // Commit the transaction to make changes permanent
    await client.query("COMMIT");
  } catch (err) {
    // Roll back the transaction if any error occurs
    // Ensures the wallet balance remains consistent
    await client.query("ROLLBACK");
    throw err; // Re-throw so the caller knows the withdrawal failed
  } finally {
    // Release the client back to the pool, regardless of success or failure
    client.release();
  }
}

/**
 * Performs a withdrawal **without transaction safety**.
 * This is unsafe under concurrent access because two withdrawals
 * can read the same balance before either writes back, causing overdrafts.
 *
 * @param userId - The ID of the user making the withdrawal
 * @param amount - The amount to withdraw
 */
export async function withdrawUnsafe(userId: number, amount: number) {
  // Get a client from the pool
  const client = await pool.connect();

  try {
    // 1. Read the current balance for the user
    const res = await client.query(
      "SELECT balance FROM wallets WHERE user_id = $1",
      [userId]
    );

    const balance = res.rows[0].balance;

    // 2. Check if balance is sufficient
    if (balance < amount) {
      throw new Error("Insufficient funds"); // Prevent negative balance
    }

    // 3. Deduct the withdrawal amount
    // ❌ Unsafe because other concurrent withdrawals may interfere
    await client.query(
      "UPDATE wallets SET balance = balance - $1 WHERE user_id = $2",
      [amount, userId]
    );
  } finally {
    // 4. Release the client back to the pool
    client.release();
  }
}
