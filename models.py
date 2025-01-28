# from sqlalchemy import Column, Integer, String
# from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from db import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     username = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)  # Hashed password



# class FoodCategory(Base):
#     __tablename__ = 'food_categories'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)  # Category name (e.g., fruits, vegetables)
#     description = Column(Text)  # A brief description of the category
    
#     foods = relationship("Food", back_populates="category")  # Relationship with Food model

# # Predefined units
# class Unit(Base):
#     __tablename__ = 'units'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)  # Unit name (e.g., kg, pieces, liters)

# # Food item model
# class Food(Base):
#     __tablename__ = 'foods'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)  # Food item name (e.g., apple, bread)
#     description = Column(Text)  # Food item description
#     price = Column(Float)  # Price of the food item
#     image_url = Column(String)  # Image URL for food item
#     quantity = Column(String)  # Quantity specification (e.g., "1 kg", "10 pieces")
#     unit_id = Column(Integer, ForeignKey('units.id'))  # Link to the predefined units
#     category_id = Column(Integer, ForeignKey('food_categories.id'))  # Link to category
#     owner_id = Column(Integer, ForeignKey('users.id'))  # Link to the user who owns the item
#     location = Column(String)  # Location of the item (street address or neighborhood)
#     latitude = Column(Float)  # Latitude of the food item (for map integration)
#     longitude = Column(Float)  # Longitude of the food item (for map integration)

#     owner = relationship("User", back_populates="foods")  # Relationship with User model
#     category = relationship("FoodCategory", back_populates="foods")  # Relationship with FoodCategory model
#     unit = relationship("Unit")  # Relationship with Unit model








from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Hashed password

    # Relationship with Food model
    foods = relationship("Food", back_populates="owner")  # Link foods created by user


class FoodCategory(Base):
    __tablename__ = 'food_categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # Category name (e.g., fruits, vegetables)
    description = Column(Text)  # A brief description of the category
    
    # Relationship with Food model
    foods = relationship("Food", back_populates="category")  # Foods in this category


# Predefined units
class Unit(Base):
    __tablename__ = 'units'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # Unit name (e.g., kg, pieces, liters)


# Food item model
class Food(Base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Food item name (e.g., apple, bread)
    description = Column(Text)  # Food item description
    # price = Column(Float)  # Price of the food item
    image_url = Column(String)  # Image URL for food item
    quantity = Column(String)  # Quantity specification (e.g., "1 kg", "10 pieces")
    unit_id = Column(Integer, ForeignKey('units.id'))  # Link to the predefined units
    category_id = Column(Integer, ForeignKey('food_categories.id'))  # Link to category
    owner_id = Column(Integer, ForeignKey('users.id'))  # Link to the user who owns the item
    location = Column(String)  # Location of the item (street address or neighborhood)
    latitude = Column(Float)  # Latitude of the food item (for map integration)
    longitude = Column(Float)  # Longitude of the food item (for map integration)

    # Relationships
    owner = relationship("User", back_populates="foods")  # Relationship with User model
    category = relationship("FoodCategory", back_populates="foods")  # Relationship with FoodCategory model
    unit = relationship("Unit")  # Relationship with Unit model



    contact = Column(String)  # Contact quantity (e.g., how many pieces or kg)
    current_time = Column(DateTime, default=datetime.now)  # The time when the food was created
    expiration_time = Column(DateTime)



class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey('users.id'))  # Donor (food owner)
    receiver_id = Column(Integer, ForeignKey('users.id'))  # Receiver (person reserving food)
    food_id = Column(Integer, ForeignKey('foods.id'))  # The food item being reserved
    reservation_time = Column(DateTime, default=datetime.now)  # Time when the reservation was made
    status = Column(String, default="pending")  # Status of the reservation (e.g., pending, confirmed)

    # Relationships
    donor = relationship("User", foreign_keys=[donor_id])  # Link to User (donor)
    receiver = relationship("User", foreign_keys=[receiver_id])  # Link to User (receiver)
    food = relationship("Food")  # Link to Food model
