import redis from "../redis";
import { db } from "../db";

/**
 * Periodic cache refresher.
 * 
 * This script runs every 30 seconds to refresh all product keys in Redis.
 * Ensures cached data stays up-to-date with the database.
 * Useful for read-heavy systems where eventual consistency is acceptable.
 */
setInterval(async () => {
  // 1. Fetch all Redis keys for products
  const keys = await redis.keys("product:*");

  for (const key of keys) {
    // 2. Extract product ID from key (format: "product:{id}")
    const id = key.split(":")[1];

    // 3. Fetch latest product data from DB
    const res = await db.query(
      "SELECT * FROM products WHERE id=$1",
      [id]
    );

    // 4. Update Redis with fresh data if product exists
    if (res.rows[0]) {
      // Set TTL to 60 seconds to prevent stale cache
      await redis.set(key, JSON.stringify(res.rows[0]), "EX", 60);
    }
  }
}, 30000); // Run every 30 seconds
