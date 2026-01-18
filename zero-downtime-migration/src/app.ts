// ------------------------
// 1. Import dependencies
// ------------------------
import express from "express";       // Express web framework
import sequelize from "./db";        // Sequelize instance for DB connection
import v1Users from "./routes/v1Users"; // Old version of user routes
import v2Users from "./routes/v2Users"; // New version of user routes

// ------------------------
// 2. Initialize Express app
// ------------------------
const app = express();

// Middleware to automatically parse incoming JSON requests
app.use(express.json());

// ------------------------
// 3. Mount route handlers
// ------------------------
// Mount v1 user routes under "/v1" prefix
app.use("/v1", v1Users);

// Mount v2 user routes under "/v2" prefix
app.use("/v2", v2Users);

// ------------------------
// 4. Start server
// ------------------------
(async () => {
  // Sync Sequelize models with the database
  // This creates tables if they don't exist
  await sequelize.sync();

  // Start Express server on port 3000
  app.listen(3000, () =>
    console.log("Server running on http://localhost:3000")
  );
})();
