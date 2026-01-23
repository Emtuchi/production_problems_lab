// LRUCache is a named export in lru-cache v7+, so we must import it directly instead of using the default import.
// This fixes the "expression is not constructable" TypeScript error.
import { LRUCache } from "lru-cache";

/**
 * In-memory "hot cache" using Least Recently Used (LRU) eviction policy.
 *
 * This cache stores frequently accessed items for very fast retrieval,
 * reducing database or external cache hits.
 */
export const hotCache = new LRUCache<string, any>({
  /**
   * Maximum number of items the cache can hold.
   * Once exceeded, the least recently used items are evicted.
   * Helps control memory usage.
   */
  max: 500,

  /**
   * Time-to-live (TTL) for each cached item in milliseconds.
   * Items expire automatically after 5 seconds to ensure freshness.
   */
  ttl: 5000
});
