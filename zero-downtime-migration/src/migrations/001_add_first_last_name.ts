// ------------------------
// 1. Import Sequelize instance
// ------------------------
import sequelize from "../db"; // Sequelize instance connected to the database

// ------------------------
// 2. Migration function
// ------------------------
async function migrate() {
  // Execute raw SQL query to alter the 'users' table
  // Adds 'first_name' and 'last_name' columns if they do not already exist
  await sequelize.query(`
    ALTER TABLE users
    ADD COLUMN IF NOT EXISTS first_name TEXT,
    ADD COLUMN IF NOT EXISTS last_name TEXT;
  `);

  // Log confirmation message after migration
  console.log("Columns added");

  // Exit the process after migration is complete
  process.exit(0);
}

// ------------------------
// 3. Run migration
// ------------------------
migrate();
