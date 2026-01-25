import express from "express";
import routes from "./routes";

const app = express(); // Create a new Express application instance

// Middleware to parse incoming JSON request bodies
// Ensures req.body contains parsed JSON
app.use(express.json());

// Mount all routes from ./routes
// This includes /withdraw/unsafe and /withdraw/safe endpoints
app.use(routes);

// Start the server on port 3000
// Logs a message when the server is ready
app.listen(3000, () => {
  console.log("Wallet service running on port 3000");
});
