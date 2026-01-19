// ------------------------
// 1. Import dependencies
// ------------------------
import User from "../models/User"; // Sequelize User model
import sequelize from "../db";     // Sequelize instance

// ------------------------
// 2. Backfill function
// ------------------------
async function backfill() {
  // Fetch all users where firstName is still null
  const users = await User.findAll({
    where: { firstName: null }
  });

  // Loop through each user
  for (const user of users) {
    // Skip users that don't have a fullName
    if (!user.fullName) continue;

    // Split fullName into parts (assumes first space separates first and last names)
    const parts = user.fullName.split(" ");
    
    // Assign firstName to the first part
    user.firstName = parts[0];

    // Assign lastName to the rest of the name, join with space, default to empty string
    user.lastName = parts.slice(1).join(" ") || "";

    // Save changes to the database
    await user.save();
  }

  // Log confirmation after processing all users
  console.log("Backfill complete");

  // Exit the process after backfill is done
  process.exit(0);
}

// ------------------------
// 3. Sync database & run backfill
// ------------------------
sequelize.sync().then(backfill); // Ensures models are in sync before running backfill
