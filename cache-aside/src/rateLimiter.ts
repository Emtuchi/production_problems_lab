import redis from "./redis";

/**
 * Simple Redis-based rate limiter.
 *
 * This function tracks the number of requests for a given key (e.g., user or IP)
 * and ensures it does not exceed a specified limit within a time window.
 *
 * @param key - Unique identifier for the entity being rate-limited
 * @param limit - Maximum allowed requests within the time window
 * @param windowSec - Duration of the rate limit window in seconds
 * @returns boolean - true if request is allowed, false if limit exceeded
 */
export async function rateLimit(
  key: string,
  limit: number,
  windowSec: number
) {
  const redisKey = `rate:${key}`;         // Redis key for counting requests
  const count = await redis.incr(redisKey); // Increment request count atomically

  if (count === 1) {
    // First request: set expiration to enforce the time window
    await redis.expire(redisKey, windowSec);
  }

  // Allow the request only if count is within the limit
  return count <= limit;
}
