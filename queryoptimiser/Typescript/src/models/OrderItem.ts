// Import necessary modules from Sequelize
import { DataTypes, Model, Optional } from "sequelize"; 
import sequelize from "../db"; // Import your Sequelize connection instance
import Order from "./Order";   // Import the Order model for relationship

// ---------------------------
// 1. Define TypeScript interfaces for strong typing
// ---------------------------

// Attributes of the OrderItem model (all DB fields)
interface OrderItemAttributes {
  id: number;        // Primary key
  orderId: number;   // Foreign key to Order
  productName: string; // Name of the product
}

// Attributes used when creating a new OrderItem
// 'id' is optional because it will be auto-incremented
interface OrderItemCreationAttributes
  extends Optional<OrderItemAttributes, "id"> {}

// ---------------------------
// 2. Define the Sequelize model class
// ---------------------------
class OrderItem
  extends Model<OrderItemAttributes, OrderItemCreationAttributes>
  implements OrderItemAttributes {
  public id!: number;          // Primary key
  public orderId!: number;     // Foreign key
  public productName!: string; // Product name

  // You could also define optional timestamps here if needed
  // public readonly createdAt!: Date;
  // public readonly updatedAt!: Date;
}

// ---------------------------
// 3. Initialize the model (map to DB table)
// ---------------------------
OrderItem.init(
  {
    id: {
      type: DataTypes.INTEGER,  // Integer column
      primaryKey: true,         // Primary key
      autoIncrement: true       // Auto-incremented
    },
    orderId: {
      type: DataTypes.INTEGER,  // Integer column for foreign key
      allowNull: false          // Cannot be null
      // Note: Index is defined below in 'indexes'
    },
    productName: {
      type: DataTypes.STRING,   // String column
      allowNull: false          // Required field
    }
  },
  {
    sequelize,                // Pass the Sequelize instance
    tableName: "order_items", // Name of the DB table
    indexes: [{ fields: ["orderId"] }] // Add index on orderId for faster queries
  }
);

// ---------------------------
// 4. Define relationships
// ---------------------------

// Each OrderItem belongs to exactly one Order
OrderItem.belongsTo(Order, { foreignKey: "orderId" });

// Each Order can have many OrderItems
Order.hasMany(OrderItem, { foreignKey: "orderId" });

// ---------------------------
// 5. Export the model
// ---------------------------
export default OrderItem;
