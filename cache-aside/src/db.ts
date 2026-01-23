import "dotenv/config";

// Import the PostgreSQL connection pool from the `pg` library.
// Pool manages multiple DB connections efficiently instead of opening
// a new connection for every request.
import { Pool } from "pg";

// Create and export a shared PostgreSQL connection pool.
// This pool will be reused across the application for all database queries.
export const db = new Pool({
  // Database connection string loaded from environment variables.
  // Keeping credentials out of code improves security and allows
  // different configs for dev, staging, and production.
  connectionString: process.env.DATABASE_URL
});
