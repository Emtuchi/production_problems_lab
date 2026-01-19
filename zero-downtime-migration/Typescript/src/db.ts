// Run "psql -U postgres -h localhost" to confirm the DB exists and you can log in after this.

// Import the Sequelize class from the sequelize package
// Sequelize is the main ORM used to communicate with the database
import { Sequelize } from "sequelize";

// Create a new Sequelize instance (database connection)
const sequelize = new Sequelize(
  "migration_demo", // Database name
  "postgres",       // Database username
  "password",       // Database password
  {
    host: "localhost", // Database host (local machine)
    dialect: "postgres", // Database type (PostgreSQL)
    logging: false       // Disable SQL query logging in the console
  }
);

// Export the Sequelize instance so it can be reused
// across models, seeders, and the server
export default sequelize;
