from fastapi import APIRouter,Request, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models import Reservation, Food
import models
from db import get_db
from auth import get_current_user, oauth2_scheme
from food import FoodStatus
from sqlalchemy.orm import Session, joinedload

router = APIRouter()

from fastapi.templating import Jinja2Templates   
templates = Jinja2Templates(directory="templates")

@router.post("/reserve/{food_id}")
async def reserve_food(
    food_id: int, 
    request: Request,
    db: Session = Depends(get_db)
):
    # Get current user (receiver)
    user = await get_current_user(request, db)

    # Fetch the food item
    food = db.query(models.Food).filter(models.Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")

    # Check if food is available
    if food.status != FoodStatus.ACTIVE:
        raise HTTPException(
            status_code=400, 
            detail=f"Food item is not available for reservation (current status: {food.status})"
        )

    # Check if user is not the donor
    if user.id == food.owner_id:
        raise HTTPException(
            status_code=400, 
            detail="You cannot reserve your own food item"
        )

    # Create reservation
    reservation = models.Reservation(
        donor_id=food.owner_id,
        receiver_id=user.id,
        food_id=food.id,
        reservation_time=datetime.now(),
        status="pending"
    )

    # Update food status
    food.status = FoodStatus.RESERVED
    
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return {
        "message": "Food item reserved successfully", 
        "reservation_id": reservation.id
    }



@router.get("/my-reservations")
async def get_my_reservations(
    request: Request,
    db: Session = Depends(get_db)
):
    user = await get_current_user(request, db)

    # Simpler query using relationship loading
    reservations = (
        db.query(models.Reservation)
        .filter(
            (models.Reservation.donor_id == user.id) | 
            (models.Reservation.receiver_id == user.id)
        )
        .options(
            joinedload(models.Reservation.food),
            joinedload(models.Reservation.donor),
            joinedload(models.Reservation.receiver)
        )
        .order_by(models.Reservation.reservation_time.desc())
        .all()
    )

    return templates.TemplateResponse(
        "reservations.html",
        {
            "request": request,
            "reservations": reservations,
            "user": user,
            "FoodStatus": FoodStatus
        }
    )































# @router.get("/my-reservations")
# async def get_my_reservations(
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     user = await get_current_user(request, db)

#     # Get reservations where user is either donor or receiver
#     reservations = (
#         db.query(models.Reservation)
#         .filter(
#             (models.Reservation.donor_id == user.id) | 
#             (models.Reservation.receiver_id == user.id)
#         )
#         .order_by(models.Reservation.reservation_time.desc())
#         .all()
#     )

#     return templates.TemplateResponse(
#         "reservations.html",
#         {
#             "request": request,
#             "reservations": reservations,
#             "user": user,
#             "FoodStatus": FoodStatus
#         }
#     )


# @router.post("/reserve/{food_id}")
# def reserve_food(food_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     # Decode the token and get the current user (receiver)
#     user = get_current_user(token, db)

#     # Fetch the food item from the database
#     food = db.query(Food).filter(Food.id == food_id).first()
#     if not food:
#         raise HTTPException(status_code=404, detail="Food item not found")

#     # Check if the user is not the donor (the person who created the food item)
#     if user.id == food.owner_id:
#         raise HTTPException(status_code=400, detail="You cannot reserve your own food item")

#     # Create the reservation
#     reservation = Reservation(
#         donor_id=food.owner_id,  # Donor is the owner of the food item
#         receiver_id=user.id,     # Receiver is the current user
#         food_id=food.id,
#         reservation_time=datetime.now(),
#         status="pending"
#     )

#     db.add(reservation)
#     db.commit()
#     db.refresh(reservation)

#     return {"message": "Food item reserved successfully", "reservation_id": reservation.id}


# @router.get("/reservations")
# def get_all_reservations(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     # Get the current user (either donor or receiver)
#     user = get_current_user(token, db)

#     # Fetch all reservations where the user is either the donor or receiver
#     reservations = db.query(Reservation).filter(
#         (Reservation.donor_id == user.id) | (Reservation.receiver_id == user.id)
#     ).all()

#     if not reservations:
#         raise HTTPException(status_code=404, detail="No reservations found")

#     return {"reservations": reservations}


# @router.put("/reservations/{reservation_id}/confirm")
# def confirm_reservation(reservation_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     user = get_current_user(token, db)
    
#     # Fetch the reservation
#     reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    
#     if not reservation:
#         raise HTTPException(status_code=404, detail="Reservation not found")

#     if reservation.donor_id != user.id:
#         raise HTTPException(status_code=403, detail="Only the donor can confirm a reservation")
    
#     reservation.status = "confirmed"
#     db.commit()
#     db.refresh(reservation)
    
#     return {"message": "Reservation confirmed", "status": reservation.status}
