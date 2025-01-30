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








from sqlalchemy import Column, Integer, String, Float,Boolean, Text, ForeignKey,DateTime
from sqlalchemy.orm import relationship, validates
from db import Base
from datetime import datetime
from datetime import datetime, timedelta
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
    

    expiration_seconds = Column(Integer)
    expiration_time = Column(DateTime)

    status = Column(String)

    # expiration_seconds = Column(Integer)
    # # expiration_time = Column(Integer)
    # expiration_time = Column(DateTime, default=lambda: datetime.now() + timedelta(seconds=expiration_seconds))  # Adding 1 hour (3600 seconds) to current time


    @validates("expiration_seconds")
    def set_expiration_time(self, key, value):
        """Automatically sets expiration_time based on expiration_seconds"""
        self.expiration_time = datetime.now() + timedelta(seconds=value)
        return value  # Return value to store in `expiration_seconds`
    

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey('users.id'))  # Donor (food owner)
    receiver_id = Column(Integer, ForeignKey('users.id'))  # Receiver (person reserving food)
    food_id = Column(Integer, ForeignKey('foods.id'))  # The food item being reserved
    reservation_time = Column(DateTime, default=datetime.now)  # Time when the reservation was made
    status = Column(String, default="pending")  # Status of the reservation (e.g., pending, confirmed)


    cancelled_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    cancelled_at = Column(DateTime, nullable=True)

    # Relationships
    donor = relationship("User", foreign_keys=[donor_id])  # Link to User (donor)
    receiver = relationship("User", foreign_keys=[receiver_id])  # Link to User (receiver)
    food = relationship("Food")  # Link to Food model

    cancelled_by = relationship("User", foreign_keys=[cancelled_by_id])

    messages = relationship("Message", back_populates="reservation")

    @property
    def unread_messages_count(self):
        return sum(1 for msg in self.messages if not msg.read and msg.receiver_id == self.receiver_id)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    read = Column(Boolean, default=False)
    
    # Relationships
    reservation = relationship("Reservation", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id], backref="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], backref="received_messages")


