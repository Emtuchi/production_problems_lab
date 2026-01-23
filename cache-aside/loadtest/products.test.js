import http from "k6/http";
import { sleep } from "k6";

// -------------------------------
// Load Test Configuration
// -------------------------------

export let options = {
  vus: 100,          // Number of virtual users to simulate concurrently
  duration: "30s"    // Total test duration
};

// -------------------------------
// Test Scenario
// -------------------------------

export default function () {
  // Send a GET request to fetch product with id=1
  // This will hit the cache-aside flow (hot cache, Redis, DB)
  http.get("http://localhost:3000/products/1");

  // Pause 1 second between requests to simulate real user think time
  sleep(1);
}
