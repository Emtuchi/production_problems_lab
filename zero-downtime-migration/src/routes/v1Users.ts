// Import Router from Express to create modular route handlers
import { Router } from "express";

// Import the User model to interact with the users table in the DB
import User from "../models/User";

// Create a new Express router instance
const router = Router();

// ------------------------
// 1. POST /users
// Create a new user in the database
// ------------------------
router.post("/users", async (req, res) => {
  // Extract fields from request body
  const { full_name, email } = req.body;

  // Create a new user in the database
  // Maps full_name from API request to fullName in the database
  const user = await User.create({
    fullName: full_name,
    email
  });

  // Respond with the newly created user as JSON
  res.json(user);
});

// ------------------------
// 2. GET /users/:id
// Fetch a user by primary key
// ------------------------
router.get("/users/:id", async (req, res) => {
  // Find user by primary key (id) from URL parameter
  const user = await User.findByPk(req.params.id);

  // Respond with a simplified JSON object
  // Use optional chaining in case user is not found
  res.json({
    id: user?.id,           // User ID or undefined if not found
    full_name: user?.fullName // User fullName or undefined
  });
});

// Export the router to be mounted in main app
export default router;
