from fastapi import APIRouter, HTTPException, Request, Depends,UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from db import get_db
from auth import get_current_user
from datetime import datetime
import uuid
from img_verify import verify_description
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


# @router.post("/foods/", response_model=schemas.Food)
# def create_food(food: schemas.FoodCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     db_food = db.query(models.Food).filter(models.Food.name == food.name).first()
#     if db_food:
#         raise HTTPException(status_code=400, detail="Food item already exists")
    
#     user = get_current_user(token, db)


#     category = db.query(models.FoodCategory).filter(models.FoodCategory.name == food.category).first()
#     unit = db.query(models.Unit).filter(models.Unit.name == food.unit).first()

#     # If category or unit doesn't exist, return an error
#     if not category:
#         raise HTTPException(status_code=400, detail="Invalid category")
#     if not unit:
#         raise HTTPException(status_code=400, detail="Invalid unit")
    

    
    
    
#     # new_food = models.Food(**food.dict(),owner_id=user.id)
    
#     new_food = models.Food(
#         name=food.name,
#         description=food.description,
#         image_url=food.image_url,
#         quantity=food.quantity,
#         category_id=category.id,  # ✅ Assign category ID
#         unit_id=unit.id,  # ✅ Assign unit ID
#         location=food.location,
#         latitude=food.latitude,
#         longitude=food.longitude,
#         contact=food.contact,
#         current_time=food.current_time or datetime.utcnow(),
#         expiration_time=food.expiration_time,
#         owner_id=user.id
#     )
    
    
#     db.add(new_food)
#     db.commit()
#     db.refresh(new_food)
#     return new_food

import os
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def update_food_status(verification_result: dict) -> str:
    """
    Updates the food status based on the description verification result.

    Args:
        verification_result (dict): The result of the description verification (contains 'is_correct').

    Returns:
        str: The updated food status ('approved' or 'under review').
    """
    # if verification_result["is_correct"] == True:
    #     return "approved"
    # else:
    #     return "under review"

    is_correct = verification_result.get("is_correct", False)  # Default to False if not found
    if is_correct:
        return "active"
    else:
        return "rejected"

from fastapi.templating import Jinja2Templates   
templates = Jinja2Templates(directory="templates")


@router.get("/add-food")
async def add_food_form(request: Request, db: Session = Depends(get_db)):
    # Get categories and units for dropdown menus
    categories = db.query(models.FoodCategory).all()
    units = db.query(models.Unit).all()
    
    return templates.TemplateResponse(
        "add_food.html",
        {
            "request": request,
            "categories": categories,
            "units": units
        }
    )



# @router.post("/foods/")
# def create_food(
#     name: str = Form(...),
#     description: str = Form(...),
#     quantity: str = Form(...),
#     category: str = Form(...),
#     unit: str = Form(...),
#     location: str = Form(...),
#     latitude: float = Form(...),
#     longitude: float = Form(...),
#     contact: str = Form(...),
#     # expiration_time: datetime = Form(...),
#     expiration_seconds: int = Form(...),
#     image: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     token: str = Depends(oauth2_scheme)
# ):
#     user = get_current_user(token, db)

#     # Save image file
#     # file_path = os.path.join(UPLOAD_DIR, image.filename)
#     # with open(file_path, "wb") as f:
#     #     f.write(image.file.read())

#     unique_filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]  # Adding the file extension
#     file_path = os.path.join(UPLOAD_DIR, unique_filename)

#     # Save the image file
#     with open(file_path, "wb") as f:
#         f.write(image.file.read())


#     description_verification = verify_description(file_path, image.filename.split('.')[-1], description)

#     print(description_verification)
#     # Check if description verification was successful or contains errors
#     # if "inaccurate" in description_verification.lower():
#     #     raise HTTPException(status_code=400, detail="Description does not match the image.")

#     llm_status = update_food_status(description_verification)
#     print(llm_status)

#     category_obj = db.query(models.FoodCategory).filter(models.FoodCategory.name == category).first()
#     unit_obj = db.query(models.Unit).filter(models.Unit.name == unit).first()

#     if not category_obj or not unit_obj:
#         raise HTTPException(status_code=400, detail="Invalid category or unit")

#     new_food = models.Food(
#         name=name,
#         description=description,
#         image_url=f"/uploads/{unique_filename}",
#         quantity=quantity,
#         category_id=category_obj.id,
#         unit_id=unit_obj.id,
#         location=location,
#         latitude=latitude,
#         longitude=longitude,
#         contact=contact,
#         expiration_seconds=expiration_seconds,
#         owner_id=user.id,
#         status=llm_status
#     )

#     db.add(new_food)
#     db.commit()
#     db.refresh(new_food)
#     return new_food

from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse


@router.post("/foods/")
async def create_food(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    quantity: str = Form(...),
    category: str = Form(...),
    unit: str = Form(...),
    location: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    contact: str = Form(...),
    expiration_seconds: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Get token from cookie
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Extract the token value
    token = token.split(" ")[1]
    
    # Get current user from token
    try:
        user = await get_current_user(request, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    # Rest of your existing code remains the same
    unique_filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(image.file.read())

    description_verification = verify_description(file_path, image.filename.split('.')[-1], description)
    print(description_verification)

    description_verification = verify_description(file_path, image.filename.split('.')[-1], description)

    print(description_verification)
    # Check if description verification was successful or contains errors
    # if "inaccurate" in description_verification.lower():
    #     raise HTTPException(status_code=400, detail="Description does not match the image.")

    llm_status = update_food_status(description_verification)
    print(llm_status)

    category_obj = db.query(models.FoodCategory).filter(models.FoodCategory.name == category).first()
    unit_obj = db.query(models.Unit).filter(models.Unit.name == unit).first()

    if not category_obj or not unit_obj:
        raise HTTPException(status_code=400, detail="Invalid category or unit")

    new_food = models.Food(
        name=name,
        description=description,
        image_url=f"/uploads/{unique_filename}",
        quantity=quantity,
        category_id=category_obj.id,
        unit_id=unit_obj.id,
        location=location,
        latitude=latitude,
        longitude=longitude,
        contact=contact,
        expiration_seconds=expiration_seconds,
        owner_id=user.id,
        status=llm_status
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    # return new_food
    # return RedirectResponse(
    #     url="/food/food-page",
    #     status_code=301  # Permanent redirect
    # )

    return JSONResponse(
        content={"message": "Food created successfully", "redirect_url": "/food/food-page"},
        status_code=status.HTTP_201_CREATED
    )


# Get all food items
# @router.get("/foods/", response_model=List[schemas.Food])
# def get_foods(db: Session = Depends(get_db)):
#     return db.query(models.Food).all()



# @router.get("/foods/", response_model=List[schemas.Food])
# def get_foods(db: Session = Depends(get_db)):
#     foods = db.query(models.Food).all()
#     return [schemas.Food.from_orm_with_relationships(food) for food in foods]  # ✅ Convert each food item



@router.get("/foods/", response_model=List[schemas.Food])
def get_foods(db: Session = Depends(get_db)):
    current_time = datetime.now()

    foods = (
        db.query(models.Food)
        .filter(models.Food.expiration_time > current_time)
        .all()
    )

    return [schemas.Food.from_orm_with_relationships(food) for food in foods]

# @router.get("/food-page")
# async def food_page(request: Request, db: Session = Depends(get_db)):
#     current_time = datetime.now()
    
#     # Get all categories for filter
#     categories = db.query(models.FoodCategory).all()
    
#     # Get all active foods
#     foods = (
#         db.query(models.Food)
#         .filter(models.Food.expiration_time > current_time)
#         .order_by(models.Food.current_time.desc())  # Latest first
#         .all()
#     )
    
#     return templates.TemplateResponse(
#         "food_items.html", 
#         {
#             "request": request,
#             "foods": foods,
#             "categories": categories,
#             "current_time": current_time
#         }
#     )



# from typing import Optional
# from datetime import datetime, timedelta
# from sqlalchemy import and_

# @router.get("/food-page")
# async def food_page(
#     request: Request,
#     category: Optional[int] = None,
#     expiration: Optional[int] = None,
#     location: Optional[str] = None,
#     status: Optional[str] = None,
#     db: Session = Depends(get_db)
# ):
#     current_time = datetime.now()
    
#     # Base query
#     query = db.query(models.Food).filter(models.Food.expiration_time > current_time)
    
#     # Apply filters
#     if category:
#         query = query.filter(models.Food.category_id == category)
    
#     if expiration:
#         # Convert hours to timedelta
#         expiry_threshold = current_time + timedelta(hours=int(expiration))
#         query = query.filter(models.Food.expiration_time <= expiry_threshold)
    
#     if location:
#         # Case-insensitive location search
#         query = query.filter(models.Food.location.ilike(f"%{location}%"))
    
#     if status:
#         query = query.filter(models.Food.status == status)
    
#     # Get all categories for filter
#     categories = db.query(models.FoodCategory).all()
    
#     # Execute query with ordering
#     foods = query.order_by(models.Food.current_time.desc()).all()
    
#     # Get current filter values for form
#     current_filters = {
#         "category": category,
#         "expiration": expiration,
#         "location": location,
#         "status": status
#     }
    
#     return templates.TemplateResponse(
#         "food_items.html", 
#         {
#             "request": request,
#             "foods": foods,
#             "categories": categories,
#             "current_time": current_time,
#             "current_filters": current_filters,
#             "FoodStatus": FoodStatus
#         }
#     )



from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy import and_

@router.get("/food-page")
async def food_page(
    request: Request,
    category: Optional[str] = None,  # Will come as string from URL
    expiration: Optional[str] = None,  # Will come as string from URL
    location: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    current_time = datetime.now()
    
    # Base query
    query = db.query(models.Food).filter(models.Food.expiration_time > current_time)
    
    # Apply category filter
    if category and category.isdigit():
        query = query.filter(models.Food.category_id == int(category))
    
    # Apply expiration filter
    if expiration and expiration.isdigit():
        hours = int(expiration)
        # Calculate the cutoff time
        cutoff_time = current_time + timedelta(hours=hours)
        # Get foods that expire before the cutoff time
        query = query.filter(
            and_(
                models.Food.expiration_time > current_time,  # Still not expired
                models.Food.expiration_time <= cutoff_time   # But expires within the window
            )
        )
    
    # Apply location filter
    if location:
        # Case-insensitive location search
        query = query.filter(models.Food.location.ilike(f"%{location}%"))
    
    # Apply status filter
    if status:
        query = query.filter(models.Food.status == status)
    
    # Get all categories for filter
    categories = db.query(models.FoodCategory).all()
    
    # Execute query with ordering
    foods = query.order_by(models.Food.current_time.desc()).all()
    
    # Get current filter values for form
    current_filters = {
        "category": int(category) if category and category.isdigit() else None,
        "expiration": int(expiration) if expiration and expiration.isdigit() else None,
        "location": location,
        "status": status
    }

    # Calculate remaining time for each food item
    for food in foods:
        food.remaining_time = food.expiration_time - current_time
    
    return templates.TemplateResponse(
        "food_items.html", 
        {
            "request": request,
            "foods": foods,
            "categories": categories,
            "current_time": current_time,
            "current_filters": current_filters,
            "FoodStatus": FoodStatus
        }
    )



from sqlalchemy.orm import Session, joinedload

# @router.get("/map")
# async def food_map(
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     current_time = datetime.now()
    
#     # Get all active foods with location data
#     foods = (
#         db.query(models.Food)
#         .filter(
#             and_(
#                 models.Food.expiration_time > current_time,
#                 models.Food.latitude.isnot(None),
#                 models.Food.longitude.isnot(None)
#             )
#         )
#         .options(
#             joinedload(models.Food.category),
#             joinedload(models.Food.unit)
#         )
#         .order_by(models.Food.current_time.desc())
#         .all()
#     )
    
#     # Convert foods to dict for JSON serialization
#     foods_data = []
#     for food in foods:
#         foods_data.append({
#             "id": food.id,
#             "name": food.name,
#             "description": food.description,
#             "image_url": food.image_url,
#             "quantity": food.quantity,
#             "location": food.location,
#             "latitude": float(food.latitude),
#             "longitude": float(food.longitude),
#             "status": food.status,
#             "category": {"id": food.category.id, "name": food.category.name},
#             "unit": {"id": food.unit.id, "name": food.unit.name}
#         })

#     return templates.TemplateResponse(
#         "food_map.html",
#         {
#             "request": request,
#             "foods": foods_data
#         }
#     )



@router.get("/map")
async def food_map(
    request: Request,
    db: Session = Depends(get_db)
):
    current_time = datetime.now()
    user = await get_current_user(request, db)
    
    # Get all active foods with location data
    foods = (
        db.query(models.Food)
        .filter(
            and_(
                models.Food.expiration_time > current_time,
                models.Food.latitude.isnot(None),
                models.Food.longitude.isnot(None)
            )
        )
        .options(
            joinedload(models.Food.category),
            joinedload(models.Food.unit),
            joinedload(models.Food.owner)
        )
        .order_by(models.Food.current_time.desc())
        .all()
    )
    
    # Convert foods to dict for JSON serialization
    foods_data = []
    for food in foods:
        remaining_time = food.expiration_time - current_time
        foods_data.append({
            "id": food.id,
            "name": food.name,
            "description": food.description,
            "image_url": food.image_url,
            "quantity": food.quantity,
            "location": food.location,
            "latitude": float(food.latitude),
            "longitude": float(food.longitude),
            "status": food.status,
            "contact": food.contact,
            "owner_name": food.owner.username,
            "category": {"id": food.category.id, "name": food.category.name},
            "unit": {"id": food.unit.id, "name": food.unit.name},
            "expiration_time": food.expiration_time.isoformat(),
            "remaining_hours": remaining_time.total_seconds() / 3600
        })

    return templates.TemplateResponse(
        "food_map.html",
        {
            "request": request,
            "foods": foods_data,
            "user": user
        }
    )


from typing import Dict, Any

@router.get("/api/foods/{food_id}")
async def get_food_details(
    food_id: int,
    request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Get current time
    current_time = datetime.now()
    
    # Get food with all related data
    food = (
        db.query(models.Food)
        .options(
            joinedload(models.Food.category),
            joinedload(models.Food.unit),
            joinedload(models.Food.owner)
        )
        .filter(models.Food.id == food_id)
        .first()
    )
    
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    # Calculate remaining time
    remaining_time = food.expiration_time - current_time
    remaining_hours = remaining_time.total_seconds() / 3600
    
    # Format expiration time
    expiry_text = ""
    if remaining_hours <= 1:
        expiry_text = f"Expires in {int(remaining_time.total_seconds() / 60)} minutes"
    elif remaining_hours <= 24:
        expiry_text = f"Expires in {int(remaining_hours)} hours"
    else:
        expiry_text = f"Expires in {int(remaining_hours / 24)} days"
    
    return {
        "id": food.id,
        "name": food.name,
        "description": food.description,
        "image_url": food.image_url,
        "quantity": food.quantity,
        "location": food.location,
        "latitude": float(food.latitude) if food.latitude else None,
        "longitude": float(food.longitude) if food.longitude else None,
        "contact": food.contact,
        "status": food.status,
        "expiration_time": food.expiration_time.isoformat(),
        "remaining_hours": remaining_hours,
        "expiry_text": expiry_text,
        "category": {
            "id": food.category.id,
            "name": food.category.name
        },
        "unit": {
            "id": food.unit.id,
            "name": food.unit.name
        },
        "owner": {
            "id": food.owner.id,
            "username": food.owner.username
        }
    }


# Add API endpoint for food details
# @router.get("/api/foods/{food_id}")
# async def get_food_details(
#     food_id: int,
#     db: Session = Depends(get_db)
# ):
#     food = (
#         db.query(models.Food)
#         .filter(models.Food.id == food_id)
#         .options(
#             joinedload(models.Food.category),
#             joinedload(models.Food.unit)
#         )
#         .first()
#     )
    
#     if not food:
#         raise HTTPException(status_code=404, detail="Food not found")
    
#     return {
#         "id": food.id,
#         "name": food.name,
#         "description": food.description,
#         "image_url": food.image_url,
#         "quantity": food.quantity,
#         "location": food.location,
#         "latitude": float(food.latitude),
#         "longitude": float(food.longitude),
#         "contact": food.contact,
#         "status": food.status,
#         "expiration_time": food.expiration_time,
#         "category": {"id": food.category.id, "name": food.category.name},
#         "unit": {"id": food.unit.id, "name": food.unit.name}
#     }



@router.get("/my-foods")
async def my_foods_page(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Get current user from token
        user = await get_current_user(request, db)
        
        # Get user's food items
        foods = (
            db.query(models.Food)
            .filter(models.Food.owner_id == user.id)
            .order_by(models.Food.current_time.desc())
            .all()
        )
        
        return templates.TemplateResponse(
            "my_foods.html",
            {
                "request": request,
                "foods": foods,
                "user": user,
                "current_time": datetime.now()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please login to view your listings"
        )
    

from enum import Enum

class FoodStatus(str, Enum):
    UNDER_REVIEW = "under_review"
    ACTIVE = "active"
    RESERVED = "reserved"
    COMPLETED = "completed"
    EXPIRED = "expired"
    REJECTED = "rejected"
    APPROVED = "approved"

# @router.get("/foods/{food_id}/details")
# async def food_detail_page(request: Request, food_id: int, db: Session = Depends(get_db)):
#     food = db.query(models.Food).filter(models.Food.id == food_id).first()
#     if not food:
#         raise HTTPException(status_code=404, detail="Food item not found")
    
#     # Get owner details
#     owner = db.query(models.User).filter(models.User.id == food.owner_id).first()
    
#     return templates.TemplateResponse(
#         "food_detail.html",
#         {
#             "request": request,
#             "food": food,
#             "owner": owner,
#             "FoodStatus": FoodStatus
#         }
#     )



@router.get("/foods/{food_id}/details")
async def food_detail_page(
    request: Request, 
    food_id: int, 
    db: Session = Depends(get_db)
):
    try:
        # Get current user
        current_user = await get_current_user(request, db)
        
        # Get food details
        food = db.query(models.Food).filter(models.Food.id == food_id).first()
        if not food:
            raise HTTPException(status_code=404, detail="Food item not found")
        
        owner = db.query(models.User).filter(models.User.id == food.owner_id).first()
        
        return templates.TemplateResponse(
            "food_detail.html",
            {
                "request": request,
                "food": food,
                "current_user": current_user,  # Pass current user to template
                "FoodStatus": FoodStatus,
                "owner": owner,
            }
        )
    except Exception as e:
        # Handle case when user is not logged in
        food = db.query(models.Food).filter(models.Food.id == food_id).first()
        if not food:
            raise HTTPException(status_code=404, detail="Food item not found")
            
        return templates.TemplateResponse(
            "food_detail.html",
            {
                "request": request,
                "food": food,
                "current_user": None,  # Pass None when user is not logged in
                "FoodStatus": FoodStatus
            }
        )
    

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


import asyncio


def update_expired_foods(db: Session):
    """
    Update status of expired food items to 'expired'
    Returns number of items updated
    """
    current_time = datetime.now()
    
    # Get all active or reserved foods that have expired
    expired_foods = (
        db.query(models.Food)
        .filter(
            models.Food.expiration_time < current_time,
            models.Food.status.in_([
                FoodStatus.ACTIVE,
                FoodStatus.RESERVED,
                FoodStatus.UNDER_REVIEW,
                FoodStatus.APPROVED
            ])
        )
        .all()
    )
    
    # Update their status to expired
    for food in expired_foods:
        food.status = FoodStatus.EXPIRED
    
    db.commit()
    return len(expired_foods)

# Function to schedule periodic updates
async def schedule_expired_foods_update():
    while True:
        try:
            db = next(get_db())
            updated_count = update_expired_foods(db)
            print(f"Updated {updated_count} expired food items")
        except Exception as e:
            print(f"Error updating expired foods: {e}")
        finally:
            await asyncio.sleep(300)  # Run every 5 minutes

# Add this to your startup events in main.py
@router.on_event("startup")
async def start_scheduler():
    asyncio.create_task(schedule_expired_foods_update())






























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