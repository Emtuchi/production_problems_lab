// Import Sequelize data types and base Model class
// Optional is used to mark fields as optional during creation
import { DataTypes, Model, Optional } from "sequelize";

// Import the shared Sequelize database connection
import sequelize from "../db";

// ------------------------
// 1. TypeScript Interfaces
// ------------------------

// Describes all attributes that exist on the User table
interface UserAttributes {
  id: number;                    // Primary key
  fullName?: string | null;      // Optional full name
  firstName?: string | null;     // Optional first name
  lastName?: string | null;      // Optional last name
  email: string;                 // Required email field
}

// Describes attributes required when creating a User
// `id` is omitted because it is auto-generated
interface UserCreationAttributes
  extends Optional<UserAttributes, "id"> {}

// ------------------------
// 2. User Model Definition
// ------------------------

// Define the User model class
// - First generic: full model attributes
// - Second generic: attributes required at creation time
class User
  extends Model<UserAttributes, UserCreationAttributes>
  implements UserAttributes {

  // These properties map directly to table columns
  public id!: number;
  public fullName!: string | null;
  public firstName!: string | null;
  public lastName!: string | null;
  public email!: string;
}

// ------------------------
// 3. Model Initialization
// ------------------------

// Initialize the model and map it to the database table
User.init(
  {
    // Primary key column
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true
    },

    // Full name column (nullable)
    fullName: {
      type: DataTypes.STRING,
      allowNull: true
    },

    // First name column (nullable)
    firstName: {
      type: DataTypes.STRING,
      allowNull: true
    },

    // Last name column (nullable)
    lastName: {
      type: DataTypes.STRING,
      allowNull: true
    },

    // Email column (required)
    email: {
      type: DataTypes.STRING,
      allowNull: false
    }
  },
  {
    sequelize,           // Sequelize instance (DB connection)
    tableName: "users"   // Explicit database table name
  }
);

// Export the model for use in queries, associations, and seeders
export default User;
