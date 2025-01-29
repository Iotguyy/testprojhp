from pydantic import BaseModel, EmailStr
import models 
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str





from pydantic import BaseModel
from typing import List, Optional

class FoodCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class FoodCategoryCreate(FoodCategoryBase):
    pass

class FoodCategory(FoodCategoryBase):
    id: int

    class Config:
        orm_mode = True

class UnitBase(BaseModel):
    name: str

class UnitCreate(UnitBase):
    pass

class Unit(UnitBase):
    id: int

    class Config:
        orm_mode = True

# class FoodBase(BaseModel):
#     name: str
#     description: Optional[str] = None
#     # price: Optional[float] = None
#     image_url: Optional[str] = None
#     quantity: str
#     location: str
#     latitude: Optional[float] = None
#     longitude: Optional[float] = None
#     category_id: int
#     unit_id: int
#     contact:str

from datetime import datetime

class FoodBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    quantity: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    category_id: int  # Ensure category is an ID
    unit_id: int  # Ensure unit is an ID
    contact: str
    current_time: Optional[datetime] = None
    expiration_time: Optional[datetime] = None


class FoodCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    quantity: str
    unit:str
    category:str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact: str
    current_time: Optional[datetime] = None
    expiration_time: Optional[datetime] = None

class Food(FoodBase):
    id: int
    owner_id: int
    status:str
    # category: str
    # unit:str


    @classmethod
    def from_orm_with_relationships(cls, food: models.Food):
        """Helper method to convert DB model to Pydantic model with category and unit names"""
        return cls(
            id=food.id,
            name=food.name,
            description=food.description,
            image_url=food.image_url,
            quantity=food.quantity,
            category=food.category.name,
            category_id=food.category_id,  # ✅ Convert category_id to name
            unit=food.unit.name,  # ✅ Convert unit_id to name
            unit_id=food.unit_id,
            location=food.location,
            latitude=food.latitude,
            longitude=food.longitude,
            contact=food.contact,
            current_time=food.current_time,
            expiration_time=food.expiration_time,
            owner_id=food.owner_id,
            status=food.status  # Add this line
        )
    


    class Config:
        orm_mode = True
