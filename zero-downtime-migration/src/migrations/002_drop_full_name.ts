// ------------------------
// 1. Import Sequelize instance
// ------------------------
import sequelize from "../db"; // Sequelize instance connected to the database

// ------------------------
// 2. Migration function
// ------------------------
async function migrate() {
  // Execute raw SQL query to drop the 'full_name' column if it exists
  await sequelize.query(`
    ALTER TABLE users
    DROP COLUMN IF EXISTS full_name;
  `);

  // Log confirmation that the column was dropped
  console.log("full_name column dropped");

  // Exit the process after migration completes
  process.exit(0);
}

// ------------------------
// 3. Call the migration function
// ------------------------
migrate();
