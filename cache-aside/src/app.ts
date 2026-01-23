import express from "express";
import productRoutes from "./routes/products";
import { register } from "./metrics";

const app = express();

// -------------------------------
// Middleware
// -------------------------------

// Parse incoming JSON requests automatically
app.use(express.json());

// -------------------------------
// Route Mounting
// -------------------------------

// Mount product-related routes under /products
// These routes handle GET/PUT operations with cache + DB
app.use("/products", productRoutes);

// Expose Prometheus metrics for monitoring
// /metrics endpoint provides real-time stats like cache hits/misses
app.get("/metrics", async (_, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

// -------------------------------
// Export App
// -------------------------------

// Export the Express app to be used in server startup
export default app;
