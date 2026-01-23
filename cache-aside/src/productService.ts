import redis from "./redis";           // Redis client for distributed caching
import { db } from "./db";             // PostgreSQL database client
import { hotCache } from "./lruCache"; // In-memory LRU cache for hot keys
import { cacheHits, cacheMisses } from "./metrics"; // Prometheus metrics

const CACHE_TTL = 60; // Cache time-to-live in seconds
const LOCK_TTL = 5;   // Lock time-to-live in seconds for stampede prevention

/**
 * Fetch a product by ID using multi-layer caching (LRU + Redis) and DB fallback.
 * Implements the cache-aside pattern with manual stampede prevention.
 */
export async function getProduct(id: number) {
  const key = `product:${id}`;   // Redis / LRU cache key
  const lockKey = `lock:${key}`; // Lock key for preventing cache stampede

  //  Check hot in-memory LRU cache first (fastest access)
  const hot = hotCache.get(key);
  if (hot) {
    cacheHits.inc(); // Increment Prometheus cache hit counter
    return hot;      // Return hot cache result immediately
  }

  // Check Redis distributed cache
  const cached = await redis.get(key);
  if (cached) {
    cacheHits.inc();                   // Cache hit in Redis
    const parsed = JSON.parse(cached); // Parse cached JSON string
    hotCache.set(key, parsed);         // Promote to hot cache
    return parsed;
  }

  // Cache miss in both caches
  cacheMisses.inc(); // Increment Prometheus cache miss counter

  // Attempt to acquire a manual lock to prevent DB stampede
  const lockAcquired = await redis.setnx(lockKey, "1"); // Set lock if not exists
  if (lockAcquired) {
    // Ensure lock expires automatically to avoid deadlocks
    await redis.expire(lockKey, LOCK_TTL);

    try {
      // Fetch fresh data from the database
      const result = await db.query(
        "SELECT * FROM products WHERE id = $1",
        [id]
      );

      if (!result.rows[0]) return null; // No product found

      // Write-through caches (Redis + hot LRU)
      const product = result.rows[0];
      await redis.set(key, JSON.stringify(product), "EX", CACHE_TTL); // Redis cache
      hotCache.set(key, product);                                     // Hot in-memory cache

      return product;
    } finally {
      // Release lock after populating cache
      await redis.del(lockKey);
    }
  } else {
    // Another process is populating cache: wait & retry
    for (let i = 0; i < 10; i++) {
      await new Promise(r => setTimeout(r, 100)); // Wait 100ms
      const retry = await redis.get(key);
      if (retry) return JSON.parse(retry); // Return once cache is populated
    }

    // Last-resort fallback: DB read after retries fail
    const fallback = await db.query(
      "SELECT * FROM products WHERE id = $1",
      [id]
    );
    if (!fallback.rows[0]) return null;

    const product = fallback.rows[0];
    // Refresh caches to reduce future DB hits
    await redis.set(key, JSON.stringify(product), "EX", CACHE_TTL);
    hotCache.set(key, product);

    return product;
  }
}

/**
 * Update a product's price and refresh caches (write-through pattern).
 */
export async function updateProduct(id: number, price: number) {
  // Update the database first
  const result = await db.query(
    "UPDATE products SET price=$1 WHERE id=$2 RETURNING *",
    [price, id]
  );

  const product = result.rows[0];
  if (!product) return null;

  // Refresh caches after update
  const key = `product:${id}`;
  await redis.set(key, JSON.stringify(product), "EX", CACHE_TTL); // Redis cache
  hotCache.set(key, product);                                     // LRU hot cache

  return product;
}
