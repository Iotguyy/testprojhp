# from fastapi import FastAPI

# app= FastAPI()

# @app.get("/")
# def home():
#     return {"msg":"vfjb"}\\



from fastapi import FastAPI
from db import Base, engine
import auth,food
import reservation

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


app.include_router(food.router, prefix="/food", tags=["Food"])

app.include_router(reservation.router, prefix="/reservation", tags=["Reservation"])

@app.get("/")
def root():
    return {"message": "Welcome to the Food Sharing Platform!"}
