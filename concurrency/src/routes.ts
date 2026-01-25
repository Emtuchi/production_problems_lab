import express from "express";
import { withdrawUnsafe, withdrawSafe } from "./wallet-service";

const router = express.Router(); // Create a new router instance

/**
 * POST /withdraw/unsafe
 * Demonstrates a withdrawal without transaction/row-lock protection.
 * May cause race conditions if multiple requests hit the same wallet simultaneously.
 */
router.post("/withdraw/unsafe", async (req, res) => {
  try {
    // Attempt to withdraw the specified amount from user 1's wallet
    await withdrawUnsafe(1, req.body.amount);

    // Respond with success if no errors occurred
    res.send("Withdrawal successful");
  } catch (e: any) {
    // Respond with HTTP 400 and the error message on failure
    res.status(400).send(e.message);
  }
});

/**
 * POST /withdraw/safe
 * Demonstrates a withdrawal using safe transactions and row locking.
 * Prevents race conditions and ensures wallet consistency under concurrent requests.
 */
router.post("/withdraw/safe", async (req, res) => {
  try {
    // Withdraw using the safe, transactional method
    await withdrawSafe(1, req.body.amount);

    // Respond with success
    res.send("Withdrawal successful");
  } catch (e: any) {
    // Respond with HTTP 400 and the error message if withdrawal fails
    res.status(400).send(e.message);
  }
});

export default router; // Export the router for use in the main Express app
