import random
import time
from fastapi import FastAPI

# Initialize FastAPI application
app = FastAPI()

@app.get("/external/profile/{user_id}")
def external_profile(user_id: int):
    """
    Simulates an external dependency (e.g., a third-party API)
    that responds with unpredictable latency.
    This is useful for testing timeouts, retries, and latency handling.
    """

    # Generate a random delay between 0.5 and 2.0 seconds
    # to mimic real-world network or service slowness
    delay = random.uniform(0.5, 2.0)

    # Block the request for `delay` seconds to simulate slow response
    time.sleep(delay)

    # Return mock profile data along with the simulated latency
    return {
        "user_id": user_id,
        "source": "external-service",
        "delay_seconds": round(delay, 2)
    }
