from pydantic import BaseModel, EmailStr

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

class FoodBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    quantity: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    category_id: int
    unit_id: int

class FoodCreate(FoodBase):
    pass

class Food(FoodBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
