import httpx

# Base URL of the external service we depend on
# In real systems, this would usually come from an environment variable
EXTERNAL_BASE_URL = "http://localhost:8001"

async def fetch_external_profile(user_id: int):
    """
    Fetch a user profile from an external service with a strict timeout.
    This protects our service from hanging if the dependency is slow.
    """

    # Define a total request timeout of 1 second
    # If the external service does not respond in time,
    # httpx will raise a timeout exception
    timeout = httpx.Timeout(1.0)

    # Create an async HTTP client with the configured timeout
    async with httpx.AsyncClient(timeout=timeout) as client:

        # Make a GET request to the external service
        response = await client.get(
            f"{EXTERNAL_BASE_URL}/external/profile/{user_id}"
        )

        # Raise an exception for non-2xx HTTP responses
        # This ensures errors are handled explicitly by the caller
        response.raise_for_status()

        # Parse and return the JSON response body
        return response.json()
