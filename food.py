from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from db import get_db
from auth import get_current_user
router = APIRouter()

# Create a food category
@router.post("/categories/", response_model=schemas.FoodCategory)
def create_category(category: schemas.FoodCategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.FoodCategory).filter(models.FoodCategory.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    new_category = models.FoodCategory(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Get all food categories
@router.get("/categories/", response_model=List[schemas.FoodCategory])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.FoodCategory).all()

# Get a specific food category by ID
@router.get("/categories/{category_id}", response_model=schemas.FoodCategory)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.FoodCategory).filter(models.FoodCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Update a food category
@router.put("/categories/{category_id}", response_model=schemas.FoodCategory)
def update_category(category_id: int, category: schemas.FoodCategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.FoodCategory).filter(models.FoodCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_category.name = category.name
    db_category.description = category.description
    db.commit()
    db.refresh(db_category)
    return db_category

# Delete a food category
@router.delete("/categories/{category_id}", response_model=schemas.FoodCategory)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.FoodCategory).filter(models.FoodCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return db_category



# Create a unit
@router.post("/units/", response_model=schemas.Unit)
def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    db_unit = db.query(models.Unit).filter(models.Unit.name == unit.name).first()
    if db_unit:
        raise HTTPException(status_code=400, detail="Unit already exists")
    
    new_unit = models.Unit(**unit.dict())
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit

# Get all units
@router.get("/units/", response_model=List[schemas.Unit])
def get_units(db: Session = Depends(get_db)):
    return db.query(models.Unit).all()

# Get a specific unit by ID
@router.get("/units/{unit_id}", response_model=schemas.Unit)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit

# Update a unit
@router.put("/units/{unit_id}", response_model=schemas.Unit)
def update_unit(unit_id: int, unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    db_unit = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    
    db_unit.name = unit.name
    db.commit()
    db.refresh(db_unit)
    return db_unit

# Delete a unit
@router.delete("/units/{unit_id}", response_model=schemas.Unit)
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    db_unit = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    
    db.delete(db_unit)
    db.commit()
    return db_unit

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/foods/", response_model=schemas.Food)
def create_food(food: schemas.FoodCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_food = db.query(models.Food).filter(models.Food.name == food.name).first()
    if db_food:
        raise HTTPException(status_code=400, detail="Food item already exists")
    
    user = get_current_user(token, db)
    
    
    
    new_food = models.Food(**food.dict(),owner_id=user.id)
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food

# Get all food items
@router.get("/foods/", response_model=List[schemas.Food])
def get_foods(db: Session = Depends(get_db)):
    return db.query(models.Food).all()

# Get a specific food item by ID
@router.get("/foods/{food_id}", response_model=schemas.Food)
def get_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")
    return food

# Update a food item
@router.put("/foods/{food_id}", response_model=schemas.Food)
def update_food(food_id: int, food: schemas.FoodCreate, db: Session = Depends(get_db)):
    db_food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Food item not found")
    
    db_food.name = food.name
    db_food.description = food.description
    db_food.price = food.price
    db_food.image_url = food.image_url
    db_food.quantity = food.quantity
    db_food.location = food.location
    db_food.latitude = food.latitude
    db_food.longitude = food.longitude
    db_food.category_id = food.category_id
    db_food.unit_id = food.unit_id
    db.commit()
    db.refresh(db_food)
    return db_food

# Delete a food item
@router.delete("/foods/{food_id}", response_model=schemas.Food)
def delete_food(food_id: int, db: Session = Depends(get_db)):
    db_food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Food item not found")
    
    db.delete(db_food)
    db.commit()
    return db_food



# Predefined categories and units
categories = [
    {"name": "Fruits", "description": "Fresh and healthy fruits"},
    {"name": "Vegetables", "description": "Organic vegetables"},
    {"name": "Baked Goods", "description": "Freshly baked breads, cakes, and pastries"},
    {"name": "Dairy Products", "description": "Milk, cheese, and other dairy items"},
    {"name": "Grains and Pasta", "description": "Rice, pasta, and other grains"},
    {"name": "Beverages", "description": "Juices, sodas, and other drinks"}
]

units = [
    {"name": "kg"},
    {"name": "pieces"},
    {"name": "liters"},
    {"name": "loaf"},
    {"name": "g"},
    {"name": "pack"}
]

@router.post("/add_categories_and_units")
def add_categories_and_units(db: Session = Depends(get_db)):
    # Add categories if they don't exist
    for category in categories:
        if not db.query(models.FoodCategory).filter(models.FoodCategory.name == category["name"]).first():
            db.add(models.FoodCategory(name=category["name"], description=category["description"]))

    # Add units if they don't exist
    for unit in units:
        if not db.query(models.Unit).filter(models.Unit.name == unit["name"]).first():
            db.add(models.Unit(name=unit["name"]))
    
    db.commit()

    return {"message": "Categories and units added successfully"}

from datetime import datetime, timedelta

@router.post("/create_foods")
def create_foods(db: Session = Depends(get_db)):
    # Fetch predefined categories and units from the database
    categories = db.query(models.FoodCategory).all()
    units = db.query(models.Unit).all()
    
    if not categories or not units:
        raise HTTPException(status_code=400, detail="Categories or Units not found")

    # Example food data to create
    # food_data = [
    #     {"name": "Apple", "description": "Fresh red apple", "price": 2.5, "quantity": "1 kg", "unit": "kg", "category": "Fruits", "location": "Store 1", "latitude": 34.0522, "longitude": -118.2437},
    #     {"name": "Banana", "description": "Ripe yellow banana", "price": 1.2, "quantity": "5 pieces", "unit": "pieces", "category": "Fruits", "location": "Store 1", "latitude": 34.0522, "longitude": -118.2437},
    #     {"name": "Carrot", "description": "Organic carrots", "price": 3.0, "quantity": "2 kg", "unit": "kg", "category": "Vegetables", "location": "Store 2", "latitude": 34.0522, "longitude": -118.2437},
    #     {"name": "Tomato", "description": "Fresh red tomatoes", "price": 4.0, "quantity": "1.5 kg", "unit": "kg", "category": "Vegetables", "location": "Store 3", "latitude": 34.0522, "longitude": -118.2437},
    #     {"name": "Bread", "description": "Freshly baked whole wheat bread", "price": 1.8, "quantity": "1 loaf", "unit": "loaf", "category": "Baked Goods", "location": "Store 4", "latitude": 34.0522, "longitude": -118.2437},
    #     {"name": "Milk", "description": "Full-fat milk", "price": 1.5, "quantity": "1 liter", "unit": "liters", "category": "Dairy Products", "location": "Store 5", "latitude": 34.0522, "longitude": -118.2437},
    #     {"name": "Yogurt", "description": "Greek yogurt", "price": 2.0, "quantity": "500 g", "unit": "g", "category": "Dairy Products", "location": "Store 5", "latitude": 34.0522, "longitude": -118.2437},
    #     {"name": "Rice", "description": "Long-grain rice", "price": 3.5, "quantity": "2 kg", "unit": "kg", "category": "Grains and Pasta", "location": "Store 6", "latitude": 34.0522, "longitude": -118.2437},
    #     {"name": "Pasta", "description": "Spaghetti pasta", "price": 2.8, "quantity": "1 pack", "unit": "pack", "category": "Grains and Pasta", "location": "Store 6", "latitude": 34.0522, "longitude": -118.2437},
    #     {"name": "Juice", "description": "Orange juice", "price": 3.0, "quantity": "1 liter", "unit": "liters", "category": "Beverages", "location": "Store 7", "latitude": 34.0522, "longitude": -118.2437}
    # ]

    # food_data = [
    # {"name": "Apple", "description": "Fresh red apple", "quantity": "1 kg", "location": "Store 1", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=7)).isoformat()},
    # {"name": "Banana", "description": "Ripe yellow banana", "quantity": "5 pieces", "location": "Store 1", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=5)).isoformat()},
    # {"name": "Carrot", "description": "Organic carrots", "quantity": "2 kg", "location": "Store 2", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=10)).isoformat()},
    # {"name": "Tomato", "description": "Fresh red tomatoes", "quantity": "1.5 kg", "location": "Store 3", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=4)).isoformat()},
    # {"name": "Bread", "description": "Freshly baked whole wheat bread", "quantity": "1 loaf", "location": "Store 4", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=3)).isoformat()},
    # {"name": "Milk", "description": "Full-fat milk", "quantity": "1 liter", "location": "Store 5", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=6)).isoformat()},
    # {"name": "Yogurt", "description": "Greek yogurt", "quantity": "500 g", "location": "Store 5", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=8)).isoformat()},
    # {"name": "Rice", "description": "Long-grain rice", "quantity": "2 kg", "location": "Store 6", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=30)).isoformat()},
    # {"name": "Pasta", "description": "Spaghetti pasta", "quantity": "1 pack", "location": "Store 6", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=20)).isoformat()},
    # {"name": "Juice", "description": "Orange juice", "quantity": "1 liter", "location": "Store 7", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=5)).isoformat()}
    # ]

    food_data = [
    {"name": "Apple", "description": "Fresh red apple", "quantity": "1 kg", "unit": "kg", "category": "Fruits", "location": "Store 1", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=7)).isoformat()},
    {"name": "Banana", "description": "Ripe yellow banana", "quantity": "5 pieces", "unit": "pieces", "category": "Fruits", "location": "Store 1", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=5)).isoformat()},
    {"name": "Carrot", "description": "Organic carrots", "quantity": "2 kg", "unit": "kg", "category": "Vegetables", "location": "Store 2", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=10)).isoformat()},
    {"name": "Tomato", "description": "Fresh red tomatoes", "quantity": "1.5 kg", "unit": "kg", "category": "Vegetables", "location": "Store 3", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=4)).isoformat()},
    {"name": "Bread", "description": "Freshly baked whole wheat bread", "quantity": "1 loaf", "unit": "loaf", "category": "Baked Goods", "location": "Store 4", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=3)).isoformat()},
    {"name": "Milk", "description": "Full-fat milk", "quantity": "1 liter", "unit": "liters", "category": "Dairy Products", "location": "Store 5", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=6)).isoformat()},
    {"name": "Yogurt", "description": "Greek yogurt", "quantity": "500 g", "unit": "g", "category": "Dairy Products", "location": "Store 5", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=8)).isoformat()},
    {"name": "Rice", "description": "Long-grain rice", "quantity": "2 kg", "unit": "kg", "category": "Grains and Pasta", "location": "Store 6", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=30)).isoformat()},
    {"name": "Pasta", "description": "Spaghetti pasta", "quantity": "1 pack", "unit": "pack", "category": "Grains and Pasta", "location": "Store 6", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=20)).isoformat()},
    {"name": "Juice", "description": "Orange juice", "quantity": "1 liter", "unit": "liters", "category": "Beverages", "location": "Store 7", "latitude": 34.0522, "longitude": -118.2437, "contact": "+1234567890", "current_time": datetime.now().isoformat(), "expiration_time": (datetime.now() + timedelta(days=5)).isoformat()}
    ]
    

    # Creating food items
    food_items = []
    for item in food_data:
        # Fetch category and unit
        category = db.query(models.FoodCategory).filter(models.FoodCategory.name == item["category"]).first()
        unit = db.query(models.Unit).filter(models.Unit.name == item["unit"]).first()

        # if not category or not unit:
        #     raise HTTPException(status_code=400, detail="Invalid category or unit")

        food_item = models.Food(
            name=item["name"],
            description=item["description"],
            # price=item["price"],
            quantity=item["quantity"],
            unit_id=unit.id,
            category_id=category.id,
            owner_id=1,  # Assuming owner with ID 1 exists
            location=item["location"],
            latitude=item["latitude"],
            longitude=item["longitude"],
            contact=item["contact"],
            current_time=datetime.fromisoformat(item["current_time"]),
            expiration_time=datetime.fromisoformat(item["expiration_time"])

        )
        food_items.append(food_item)

    # Add all food items to the session and commit
    db.add_all(food_items)
    db.commit()
    # db.refresh(food_items)

    return {"message": "10 food items created successfully", "food_items": len(food_items)}