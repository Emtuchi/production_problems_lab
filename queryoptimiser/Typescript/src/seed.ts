// ------------------------
// 1. Import dependencies
// ------------------------
import { faker } from "@faker-js/faker";   // Faker for generating fake data
import sequelize from "./db";               // Sequelize instance
import User from "./models/User";           // User model
import Order from "./models/Order";         // Order model
import OrderItem from "./models/OrderItem"; // OrderItem model

// ------------------------
// 2. Seed function
// ------------------------
async function seed() {
  // Sync all models with the database
  // `force: true` drops existing tables and recreates them
  await sequelize.sync({ force: true });

  console.log("Database synced. Seeding data...");

  // ------------------------
  // Constants
  // ------------------------
  const NUM_USERS = 2000;
  const ORDERS_PER_USER = 10;
  const ITEMS_PER_ORDER = 5;

  // ------------------------
  // Step 1: Generate all users
  // ------------------------
  const usersData = Array.from({ length: NUM_USERS }, () => ({
    name: faker.name.fullName()
  }));

  // Bulk insert users and get inserted rows with IDs
  const users = await User.bulkCreate(usersData, { returning: true });

  // ------------------------
  // Step 2: Generate all orders
  // ------------------------
  const ordersData: { userId: number }[] = [];
  for (const user of users) {
    for (let j = 0; j < ORDERS_PER_USER; j++) {
      ordersData.push({ userId: user.id });
    }
  }

  // Bulk insert orders and get inserted rows with IDs
  const orders = await Order.bulkCreate(ordersData, { returning: true });

  // ------------------------
  // Step 3: Generate all order items
  // ------------------------
  const itemsData: { orderId: number; productName: string }[] = [];
  for (const order of orders) {
    for (let k = 0; k < ITEMS_PER_ORDER; k++) {
      itemsData.push({
        orderId: order.id,
        productName: faker.commerce.productName()
      });
    }
  }

  // Bulk insert all items
  await OrderItem.bulkCreate(itemsData);

  console.log("Database seeded successfully!");
  process.exit(0); // Exit process after seeding
}

// ------------------------
// 3. Run the seed function
// ------------------------
seed().catch((err) => {
  console.error("Seeding failed:", err);
  process.exit(1);
});
