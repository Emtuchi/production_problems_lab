import { Pool } from "pg"; 
// Import PostgreSQL connection pool.
// Pool manages multiple DB connections efficiently instead of opening a new one per query.

export const pool = new Pool({
  // Connection string loaded from environment variables (.env)
  // Example: postgresql://user:password@localhost:5432/db_name
  connectionString: process.env.DATABASE_URL,
});
