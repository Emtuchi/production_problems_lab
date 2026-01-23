import client from "prom-client";

/**
 * Create a custom Prometheus registry.
 *
 * Using a registry allows us to:
 * - group related metrics together
 * - expose only the metrics we care about
 * - avoid conflicts with default/global registries
 */
export const register = new client.Registry();

/**
 * Collect default Node.js process metrics:
 * - CPU usage
 * - memory usage
 * - event loop lag
 * - GC stats
 *
 * These metrics are critical for understanding
 * system health and performance under load.
 */
client.collectDefaultMetrics({ register });

/**
 * Counter for cache hits.
 *
 * Increments every time a request is served
 * directly from the cache instead of the database.
 * High cache hit rate = lower latency and DB load.
 */
export const cacheHits = new client.Counter({
  name: "cache_hits_total",
  help: "Total number of cache hits"
});

/**
 * Counter for cache misses.
 *
 * Increments when data is not found in cache
 * and the system must fall back to the database.
 * Useful for calculating cache efficiency.
 */
export const cacheMisses = new client.Counter({
  name: "cache_misses_total",
  help: "Total number of cache misses"
});

/**
 * Register custom metrics with Prometheus.
 *
 * Without registering them, Prometheus
 * would not be able to scrape or expose them.
 */
register.registerMetric(cacheHits);
register.registerMetric(cacheMisses);
