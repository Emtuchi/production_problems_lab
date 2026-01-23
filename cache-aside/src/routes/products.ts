import { Router } from "express";
import { getProduct, updateProduct } from "../productService";
import { rateLimit } from "../rateLimiter";

const router = Router();

/**
 * GET /:id
 * Fetch a product by ID with rate limiting.
 */
router.get("/:id", async (req, res) => {
  // 1. Apply rate limiting per client IP
  //    Allows 10 requests per 5 seconds
  const allowed = await rateLimit(req.ip!, 10, 5);
  if (!allowed) return res.status(429).json({ error: "Too many requests" });

  // 2. Fetch product from service (handles cache + DB)
  const product = await getProduct(Number(req.params.id));
  
  // 3. Return 404 if product not found
  if (!product) return res.sendStatus(404);

  // 4. Return product data
  res.json(product);
});

/**
 * PUT /:id
 * Update product price and write-through to cache + DB.
 */
router.put("/:id", async (req, res) => {
  // 1. Update product via service
  const product = await updateProduct(
    Number(req.params.id),
    req.body.price
  );

  // 2. Return updated product data
  res.json(product);
});

export default router;
