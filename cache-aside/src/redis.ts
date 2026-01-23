import Redis from "ioredis";

/**
 * Create a Redis client.
 *
 * This supports TWO deployment modes:
 * 1. Redis Cluster (for horizontal scaling & high availability)
 * 2. Single Redis instance (simpler local/dev setup)
 */
const redis =
  // If running in Redis Cluster mode
  process.env.REDIS_CLUSTER === "true"
    ? new Redis.Cluster([
        /**
         * List of Redis cluster nodes.
         * The client connects to any node and discovers the full cluster topology.
         * This allows automatic request routing, failover, and slot rebalancing.
         */
        { host: "127.0.0.1", port: 7000 },
        { host: "127.0.0.1", port: 7001 },
        { host: "127.0.0.1", port: 7002 }
      ])
    : new Redis(
        /**
         * Fallback to a single Redis instance.
         * Commonly used in local development or simple deployments.
         *
         * Example REDIS_URL:
         * redis://localhost:6379
         */
        process.env.REDIS_URL!
      );

/**
 * Export a shared Redis client instance.
 *
 * Using a single client:
 * - avoids opening unnecessary connections
 * - improves performance
 * - simplifies cache usage across the app
 */
export default redis;
