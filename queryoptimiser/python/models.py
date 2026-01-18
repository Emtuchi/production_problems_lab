from sqlalchemy import Column, Integer, String, ForeignKey  # Import column types and foreign key support
from sqlalchemy.orm import relationship  # Import ORM relationship for associations between tables
from sqlalchemy import Index  # Import Index (not used here explicitly, but could define custom indexes)
from database import Base  # Base class for declarative SQLAlchemy models (from your database.py)

# Note: An index is like a table of contents for your database.
#  
# Just like a book’s table of contents lets you jump to the right page without reading every page,
# An index lets the database find rows faster without scanning the whole table.

# ---------------------------
# User model
# ---------------------------
class User(Base):
    __tablename__ = "users"  # Table name in the database
    id = Column(Integer, primary_key=True)  # Primary key column, auto-incremented integer
    name = Column(String)  # User's name column

    # Define a one-to-many relationship to Order
    # - "Order" refers to the Order class (string because defined later)
    # - back_populates links back to User in the Order class
    orders = relationship("Order", back_populates="user")

# ---------------------------
# Order model
# ---------------------------
class Order(Base):
    __tablename__ = "orders"  # Table name
    id = Column(Integer, primary_key=True)  # Primary key for orders
    # Foreign key to users.id
    # index=True automatically creates an index on user_id for faster queries filtering by user
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    # Relationship back to the parent User
    user = relationship("User", back_populates="orders")
    # One-to-many relationship to OrderItem
    items = relationship("OrderItem", back_populates="order")

# ---------------------------
# OrderItem model
# ---------------------------
class OrderItem(Base):
    __tablename__ = "order_items"  # Table name
    id = Column(Integer, primary_key=True)  # Primary key
    # Foreign key to orders.id
    # index=True speeds up lookups of items by order_id
    order_id = Column(Integer, ForeignKey("orders.id"), index=True)
    product_name = Column(String)  # Name of the product in the order item

    # Relationship back to the parent Order
    order = relationship("Order", back_populates="items")
