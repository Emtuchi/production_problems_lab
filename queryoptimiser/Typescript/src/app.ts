// ------------------------
// 1. Import dependencies
// ------------------------
import express, { Request, Response } from "express"; // Express web framework
import sequelize from "./db";                         // Sequelize instance
import User from "./models/User";                     // User model
import Order from "./models/Order";                   // Order model
import OrderItem from "./models/OrderItem";           // OrderItem model

// ------------------------
// 2. Initialize Express app
// ------------------------
const app = express();
const PORT = 3000; // Server port

// ------------------------
// 3. SLOW ENDPOINT (N+1 problem)
// ------------------------
app.get("/users/:id/orders", async (req: Request, res: Response) => {
  const start = Date.now(); // Start timer to measure query time

  // Convert route param to number (important for TypeScript + Sequelize)
  const userId = Number(req.params.id);
  if (isNaN(userId)) {
    return res.status(400).json({ error: "Invalid user id" });
  }

  // Fetch user by primary key
  const user = await User.findByPk(userId);
  if (!user) return res.status(404).json({ error: "User not found" });

  // Fetch all orders for this user
  const orders = await Order.findAll({ where: { userId: user.id } });

  const result = [];

  // For each order, fetch all items → causes N+1 queries
  for (const order of orders) {
    const items = await OrderItem.findAll({
      where: { orderId: order.id }
    });

    result.push({
      orderId: order.id,
      items: items.map(i => i.productName)
    });
  }

  // Respond with JSON including query duration
  res.json({
    query_time_ms: Date.now() - start,
    orders: result
  });
});

// ------------------------
// 4. FAST ENDPOINT (Eager Loading / JOINs)
// ------------------------
app.get("/users/:id/orders-fast", async (req: Request, res: Response) => {
  const start = Date.now(); // Start timer

  // Convert route param to number
  const userId = Number(req.params.id);
  if (isNaN(userId)) {
    return res.status(400).json({ error: "Invalid user id" });
  }

  // Fetch user with eager-loaded relations
  const user = await User.findByPk(userId, {
    include: {
      model: Order,
      include: [OrderItem]
    }
  });

  if (!user) return res.status(404).json({ error: "User not found" });

  // Map nested Sequelize result into clean JSON
  const orders = (user as any).Orders.map((order: any) => ({
    orderId: order.id,
    items: order.OrderItems.map((i: any) => i.productName)
  }));

  // Respond with JSON including query duration
  res.json({
    query_time_ms: Date.now() - start,
    orders
  });
});

// ------------------------
// 5. Connect to DB and start server
// ------------------------
sequelize.authenticate().then(() => {
  console.log("DB connected");
  app.listen(PORT, () => console.log(`Server running on ${PORT}`));
});
