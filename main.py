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
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables
Base.metadata.create_all(bind=engine)

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


app.include_router(food.router, prefix="/food", tags=["Food"])

app.include_router(reservation.router, prefix="/reservation", tags=["Reservation"])

@app.get("/")
def root():
    return {"message": "Welcome to the Food Sharing Platform!"}


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

