from fastapi import FastAPI
from app.client import fetch_external_profile
from app.fallback import fallback_profile
from app.utils import now_ms
import httpx

# Initialize the FastAPI application
app = FastAPI()

@app.get("/profile/{user_id}")
async def get_profile(user_id: int):
    """
    Main API endpoint.
    Demonstrates how slow or unreliable downstream services
    directly impact end-to-end request latency.
    """

    # Record request start time for latency measurement
    start = now_ms()

    try:
        # Attempt to fetch data from an external dependency
        # This call may be slow or time out
        external_data = await fetch_external_profile(user_id)
        source = "external"  # Track where the data came from

    except httpx.RequestError:
        # Handle network errors or timeouts gracefully
        # Instead of failing the request, return fallback data
        external_data = fallback_profile(user_id)
        source = "fallback"

    # Calculate total request duration in milliseconds
    duration = round(now_ms() - start, 2)

    # Return response with observability-friendly metadata
    return {
        "user_id": user_id,                # Requested user
        "data": external_data,             # Profile data (external or fallback)
        "source_used": source,              # Indicates which path was taken
        "total_latency_ms": duration        # End-to-end request latency
    }
