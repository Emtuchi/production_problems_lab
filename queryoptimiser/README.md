# Resolved N+1 query issues in a Node.js + PostgreSQL backend, adding indexes and eager loading to reduce API query time by ~97% on 100k+ records in Typescript and python

## Explanation:

Initially, fetching a user’s orders and items was very slow because it triggered an N+1 problem: for every order, a separate query ran to fetch items.

### I optimized it by:

### A. Adding indexes on foreign keys (userId and orderId)

- Without an index, the database may have to scan the entire table (full table scan) to find matching rows.

- With an index, the database can jump directly to the relevant rows.

- **Analogy:**\
  If your table is a book, an index is like the book’s index at the back—it lets you quickly find a topic instead of reading every page.

### B. Using eager loading to fetch related orders and items in a single query

- **1. Avoids the N+1 query problem**
  - Without eager loading, fetching a parent and its related children often triggers one query for the parent + one query per child.

  - **Example:**\
    Fetching 100 orders and their items → 1 query for orders + 100 queries for items.

  - With eager loading, the database can fetch orders and all their items in a single query (or a small number of optimized queries).

**2. Reduces latency**

- Fewer queries mean less round-trip time to the database, which is crucial when the app is under load or when tables have millions of rows.

**3. Optimizes joins**

- Eager loading uses SQL JOINs or optimized queries to fetch related data all at once.

- **Example:**\
  SELECT \* FROM orders LEFT JOIN order_items ON orders.id = order_items.order_id WHERE orders.user_id = 42
