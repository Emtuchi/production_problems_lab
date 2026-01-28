def fallback_profile(user_id: int):
    """
    Return a safe fallback response when the external service
    is slow, down, or times out.
    """

    # Provide minimal but valid data so the system
    # can continue functioning without failing hard
    return {
        "user_id": user_id,              # Preserve the requested user identifier
        "source": "fallback",             # Indicates this data did NOT come from the external service
        "note": "External service unavailable, using fallback data"
                                         # Useful for debugging, logging, and observability
    }
