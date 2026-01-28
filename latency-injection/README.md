# Latency injection

Latency injection is when you artificially delay certain parts of your system, like a database query or an API call, to simulate slow responses.

**For example:**\
A service that usually responds in 50ms might be delayed to 500ms or 1s randomly during testing.

## Why it makes systems better

1. Reveals hidden weaknesses
   - Slowdowns in one part of a system can cause cascading failures if untested.

   - Injecting latency shows where timeouts, retries, or bottlenecks might occur before it happens in production.

2. Tests fallback and resilience mechanisms
   - In your project, if an external service is slow, the fallback logic kicks in.

   - Latency injection ensures the fallback actually works under real “slow dependency” conditions.

3. Prevents surprises in production
   - You can observe how your system behaves under stress.

   - Helps set realistic timeouts, retry policies, and error handling.

4. Encourages better design
   - Forces developers to think about asynchronous calls, caching, and service degradation.

   - Promotes robust, resilient, and user-friendly systems.

## Run Project

1.  Install dependencies
    ```
    pip install -r requirements.txt
    ```
2.  Start external service (first)
    ```
    uvicorn app.external:app --port 8001
    ```
3.  Start main API (second)
    ```
    uvicorn app.main:app --port 8000
    ```
4.  Test API
    ```
    curl http://localhost:8000/profile/1
    ```
