import time  # Provides access to system time utilities

def now_ms() -> float:
    """
    Return the current time in milliseconds.

    Useful for:
    - Measuring latency
    - Benchmarking performance
    - Logging timestamps with higher precision than seconds
    """
    # time.time() returns the current time in seconds since the Unix epoch
    # Multiply by 1000 to convert seconds → milliseconds
    return time.time() * 1000
