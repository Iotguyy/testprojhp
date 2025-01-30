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







@router.put("/reservations/{reservation_id}/confirm")
async def confirm_reservation(
    reservation_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = await get_current_user(request, db)
    
    # Get reservation with related food item
    reservation = (
        db.query(models.Reservation)
        .filter(models.Reservation.id == reservation_id)
        .options(joinedload(models.Reservation.food))
        .first()
    )
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Only donor can confirm
    if reservation.donor_id != user.id:
        raise HTTPException(status_code=403, detail="Only the donor can confirm a reservation")
    
    # Check if reservation is pending
    if reservation.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending reservations can be confirmed")
    
    # Update reservation and food status
    reservation.status = "confirmed"
    reservation.food.status = FoodStatus.COMPLETED
    
    db.commit()
    
    return {"message": "Reservation confirmed successfully"}

@router.put("/reservations/{reservation_id}/cancel")
async def cancel_reservation(
    reservation_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = await get_current_user(request, db)
    
    # Get reservation with related food item
    reservation = (
        db.query(models.Reservation)
        .filter(models.Reservation.id == reservation_id)
        .options(joinedload(models.Reservation.food))
        .first()
    )
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Check if user is either donor or receiver
    if user.id not in [reservation.donor_id, reservation.receiver_id]:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this reservation")
    
    # Check if reservation can be cancelled
    if reservation.status not in ["pending", "confirmed"]:
        raise HTTPException(status_code=400, detail="This reservation cannot be cancelled")
    
    # Update reservation and food status
    reservation.status = "cancelled"
    reservation.food.status = FoodStatus.ACTIVE  # Make food available again
    
    # Add cancellation details
    reservation.cancelled_by_id = user.id
    reservation.cancelled_at = datetime.now()
    
    db.commit()
    
    return {"message": "Reservation cancelled successfully"}

@router.put("/reservations/{reservation_id}/no-show")
async def mark_no_show(
    reservation_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = await get_current_user(request, db)
    
    reservation = (
        db.query(models.Reservation)
        .filter(models.Reservation.id == reservation_id)
        .options(joinedload(models.Reservation.food))
        .first()
    )
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Only donor can mark no-show
    if reservation.donor_id != user.id:
        raise HTTPException(status_code=403, detail="Only the donor can mark no-show")
    
    if reservation.status != "confirmed":
        raise HTTPException(status_code=400, detail="Only confirmed reservations can be marked as no-show")
    
    reservation.status = "no_show"
    reservation.food.status = FoodStatus.ACTIVE
    
    db.commit()
    
    return {"message": "Reservation marked as no-show"}




from fastapi import WebSocket
from typing import List


from pydantic import BaseModel

class MessageCreate(BaseModel):
    content: str

@router.post("/reservations/{reservation_id}/messages")
async def send_message(
    reservation_id: int,
    message: MessageCreate,  # Changed this
    request: Request,
    db: Session = Depends(get_db)
):
    user = await get_current_user(request, db)
    
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # Verify user is part of the reservation
    if user.id not in [reservation.donor_id, reservation.receiver_id]:
        raise HTTPException(status_code=403, detail="Not authorized to send messages for this reservation")
    
    # Determine receiver
    receiver_id = reservation.donor_id if user.id == reservation.receiver_id else reservation.receiver_id
    
    new_message = models.Message(
        reservation_id=reservation_id,
        sender_id=user.id,
        receiver_id=receiver_id,
        content=message.content  # Use the content from the request body
    )
    
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return {"message": "Message sent successfully"}


# Message endpoints
# @router.post("/reservations/{reservation_id}/messages")
# async def send_message(
#     reservation_id: int,
#     content: str,
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     user = await get_current_user(request, db)
    
#     reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
#     if not reservation:
#         raise HTTPException(status_code=404, detail="Reservation not found")
    
#     # Verify user is part of the reservation
#     if user.id not in [reservation.donor_id, reservation.receiver_id]:
#         raise HTTPException(status_code=403, detail="Not authorized to send messages for this reservation")
    
#     # Determine receiver
#     receiver_id = reservation.donor_id if user.id == reservation.receiver_id else reservation.receiver_id
    
#     message = models.Message(
#         reservation_id=reservation_id,
#         sender_id=user.id,
#         receiver_id=receiver_id,
#         content=content
#     )
    
#     db.add(message)
#     db.commit()
#     db.refresh(message)
    
#     return {"message": "Message sent successfully"}

@router.get("/reservations/{reservation_id}/messages")
async def get_messages(
    reservation_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = await get_current_user(request, db)
    
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    if user.id not in [reservation.donor_id, reservation.receiver_id]:
        raise HTTPException(status_code=403, detail="Not authorized to view these messages")
    
    messages = (
        db.query(models.Message)
        .filter(models.Message.reservation_id == reservation_id)
        .order_by(models.Message.created_at.asc())
        .options(joinedload(models.Message.sender))
        .all()
    )
    
    # Mark unread messages as read
    unread_messages = [
        msg for msg in messages 
        if msg.receiver_id == user.id and not msg.read
    ]
    for msg in unread_messages:
        msg.read = True
    db.commit()
    
    return templates.TemplateResponse(
        "messages.html",
        {
            "request": request,
            "messages": messages,
            "reservation": reservation,
            "current_user": user
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
