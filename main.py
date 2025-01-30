# from fastapi import FastAPI

# app= FastAPI()

# @app.get("/")
# def home():
#     return {"msg":"vfjb"}\\



from fastapi import FastAPI, Request
from db import Base, engine
import auth,food
import reservation
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from auth import get_current_user
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from db import get_db


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Create tables
Base.metadata.create_all(bind=engine)

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


app.include_router(food.router, prefix="/food", tags=["Food"])

app.include_router(reservation.router, prefix="/reservation", tags=["Reservation"])

@app.get("/")
def root(request: Request):
    # return {"message": "Welcome to the Food Sharing Platform!"}
    return templates.TemplateResponse("home_page.html", {"request": request})


templates = Jinja2Templates(directory="templates")

@app.get("/i")
def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register")
def serve_homepages(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/fooditem")
def serve_homepages(request: Request):
    return templates.TemplateResponse("food.html", {"request": request})

from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Food, User
from fastapi.responses import RedirectResponse
from datetime import datetime


@app.get("/profile")
async def profile_page(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Get current user using the existing function
        user = await get_current_user(request, db)
        
        current_time = datetime.now()
        
        # Get user statistics
        stats = {
            "total_foods": db.query(func.count(Food.id)).filter(Food.owner_id == user.id).scalar(),
            "active_foods": db.query(func.count(Food.id))
                .filter(Food.owner_id == user.id, Food.status == "active").scalar() or 0,
            "expired_foods": db.query(func.count(Food.id))
                .filter(
                    Food.owner_id == user.id,
                    Food.expiration_time < current_time
                ).scalar() or 0,
            "available_foods": db.query(func.count(Food.id))
                .filter(
                    Food.owner_id == user.id,
                    Food.expiration_time > current_time,
                    food.status == "rejected"
                ).scalar() or 0
        }
        
        # Get user's recent foods
        recent_foods = (
            db.query(Food)
            .filter(Food.owner_id == user.id,
            )
            .order_by(Food.current_time.desc())
            .limit(5)
            .all()
        )
        
        return templates.TemplateResponse(
            "profile.html",
            {
                "request": request,
                "user": user,
                "stats": stats,
                "recent_foods": recent_foods,
                "now": current_time  # Pass current time to template
            }
        )
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            return RedirectResponse(url="/auth/login", status_code=302)
        raise e