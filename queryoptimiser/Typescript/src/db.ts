// Import the Sequelize constructor from the 'sequelize' package
import { Sequelize } from "sequelize";

// Create a new Sequelize instance to connect to the database
// initialise postgres "sudo -u postgres psql", then fill these details in
// dont use capital letters for names of anything
const sequelize = new Sequelize(
  "db",                // Database name, make sure its the name u input when u create the d.b
  "postgres",          // Database username
  "password",          // Database password, create your db with this password
  {
    host: "localhost",  // Hostname where the DB is running
    dialect: "postgres", // Database type (PostgreSQL in this case)
    logging: false       // Disable SQL query logging to console
  }
);

// Export the Sequelize instance for use in other files
export default sequelize;
