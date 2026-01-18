from faker import Faker               # Import Faker to generate fake data
from database import SessionLocal     # Import session factory to interact with the DB
from models import User, Order, OrderItem  # Import ORM models (tables)

# Initialize Faker to generate random names, words, etc.
fake = Faker()

# Create a new database session
db = SessionLocal()

# Define how much fake data we want to generate
NUM_USERS = 2000          # Number of users to create
ORDERS_PER_USER = 10      # Number of orders per user
ITEMS_PER_ORDER = 5       # Number of items per order

# Loop to create users
for _ in range(NUM_USERS):
    # Create a new User instance with a random name
    user = User(name=fake.name())
    db.add(user)           # Add the user to the session (not yet committed)
    db.flush()             # Flush to the DB to assign an ID to the user
                           # (needed for foreign key in orders)

    # Loop to create orders for this user
    for _ in range(ORDERS_PER_USER):
        order = Order(user_id=user.id)  # Associate order with current user
        db.add(order)                   # Add order to session
        db.flush()                      # Flush to get order.id for items

        # Loop to create items for this order
        for _ in range(ITEMS_PER_ORDER):
            item = OrderItem(
                order_id=order.id,        # Associate item with current order
                product_name=fake.word()  # Generate a random product name
            )
            db.add(item)                  # Add item to session

# Commit all changes to the database
# This writes all users, orders, and items permanently
db.commit()

# Close the session to free up resources
db.close()

# Print confirmation message
print("Database seeded.")
