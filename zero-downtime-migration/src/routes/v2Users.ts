// Import Router from Express to create modular route handlers
import { Router } from "express";

// Import the User model to interact with the users table in the database
import User from "../models/User";

// Create a new Express router instance
const router = Router();

// ------------------------
// NEW API — Create a user
// ------------------------
router.post("/users", async (req, res) => {
  // Extract first name, last name, and email from the request body
  const { first_name, last_name, email } = req.body;

  // Combine first and last name into a single fullName string
  const fullName = `${first_name} ${last_name}`;

  // Create a new user in the database
  // Writes both individual names and fullName for convenience (dual write)
  const user = await User.create({
    firstName: first_name,  // Maps API first_name to DB column firstName
    lastName: last_name,    // Maps API last_name to DB column lastName
    fullName,               // Store full name in DB as well
    email                   // Store email
  });

  // Respond with the newly created user object as JSON
  res.json(user);
});

// ------------------------
// NEW API — Get a user by ID
// ------------------------
router.get("/users/:id", async (req, res) => {
  // Find user in the database by primary key (id from URL parameter)
  const user = await User.findByPk(req.params.id);

  // Respond with selected fields using optional chaining
  // Ensures no error if user is not found
  res.json({
    id: user?.id,              // User ID or undefined
    first_name: user?.firstName, // User firstName or undefined
    last_name: user?.lastName    // User lastName or undefined
  });
});

// Export the router so it can be mounted in the main Express app
export default router;
