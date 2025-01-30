# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from db import get_db
# from models import User
# from schemas import UserCreate, Token
# from utils import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
# import datetime
# import jwt
# import os

# router = APIRouter()


# from fastapi import Form
# from fastapi.templating import Jinja2Templates
# from fastapi import Request

# templates = Jinja2Templates(directory="templates")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# # Register User
# # @router.post("/register", response_model=Token)
# # def register(user: UserCreate, db: Session = Depends(get_db)):
# #     existing_user = db.query(User).filter(User.email == user.email).first()
# #     if existing_user:
# #         raise HTTPException(status_code=400, detail="Email already registered")

# #     hashed_password = hash_password(user.password)
# #     new_user = User(email=user.email, username=user.username, password=hashed_password)
# #     db.add(new_user)
# #     db.commit()
# #     db.refresh(new_user)

# #     token = create_access_token({"sub": new_user.email}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
# #     return {"access_token": token, "token_type": "bearer"}


# # @router.post("/register")
# # def register(user: UserCreate, db: Session = Depends(get_db)):
# #     existing_user = db.query(User).filter(User.email == user.email).first()
# #     if existing_user:
# #         raise HTTPException(status_code=400, detail="Email already registered")

# #     hashed_password = hash_password(user.password)
# #     new_user = User(email=user.email, username=user.username, password=hashed_password)
# #     db.add(new_user)
# #     db.commit()
# #     db.refresh(new_user)

# #     return {"message": "User registered successfully. Please log in."}  # No token returned



# # # Login User
# # @router.post("/login", response_model=Token)
# # def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
# #     user = db.query(User).filter(User.email == form_data.username).first()
    
# #     if not user or not verify_password(form_data.password, user.password):
# #         raise HTTPException(status_code=400, detail="Invalid credentials")

# #     token = create_access_token({"sub": user.email}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
# #     return {"access_token": token, "token_type": "bearer"}




# @router.get("/register-page")
# def register_page(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})

# @router.get("/login-page")
# def login_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @router.post("/register")
# def register(
#     email: str = Form(...),
#     username: str = Form(...),
#     password: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     existing_user = db.query(User).filter(User.email == email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = hash_password(password)
#     new_user = User(email=email, username=username, password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message": "User registered successfully. Please log in."}

# @router.post("/login")
# def login(
#     email: str = Form(...),
#     password: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     user = db.query(User).filter(User.email == email).first()
    
#     if not user or not verify_password(password, user.password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     token = create_access_token({"sub": user.email}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     return {"access_token": token, "token_type": "bearer"}


# # Get Current User
# @router.get("/me")
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, os.getenv("SECRET_KEY", "mysecret"), algorithms=["HS256"])
#         email = payload.get("sub")
#         user = db.query(User).filter(User.email == email).first()

#         if not user:
#             raise HTTPException(status_code=400, detail="User not found")
        
#         # return {"email": user.email, "username": user.username}
#         print(user)
#         return user

#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")









from fastapi import APIRouter, Depends,Form, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db import get_db
from models import User
from schemas import UserCreate, Token
from utils import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.templating import Jinja2Templates
import datetime
import jwt
import os
from fastapi import APIRouter, Depends, Form, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from db import get_db
from models import User
from schemas import UserCreate, Token
from utils import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.templating import Jinja2Templates
import datetime
import jwt
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/register-page")
async def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html", 
        {"request": request, "error": None}
    )

@router.get("/login-page")
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "error": None}
    )

@router.post("/register")
async def register(
    request: Request,
    response: Response,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "error": "Email already registered"}
            )

        hashed_password = hash_password(password)
        new_user = User(email=email, username=username, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return RedirectResponse(
            url="/auth/login-page",
            status_code=status.HTTP_303_SEE_OTHER
        )

    except Exception as e:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": str(e)}
        )

# @router.post("/login")
# async def login(
#     request: Request,
#     response: Response,
#     email: str = Form(...),
#     password: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     try:
#         user = db.query(User).filter(User.email == email).first()
        
#         if not user or not verify_password(password, user.password):
#             return templates.TemplateResponse(
#                 "login.html",
#                 {"request": request, "error": "Invalid credentials"}
#             )

#         # Create access token
#         token = create_access_token(
#             {"sub": user.email},
#             datetime.timedelta(minutes=30)
#         )

#         # Create response with redirect
#         # response = RedirectResponse(
#         #     url="/food/fooditem",  # Redirect to dashboard or home page
#         #     status_code=status.HTTP_303_SEE_OTHER
#         # )

#         # Set secure cookie
#         response.set_cookie(
#             key="access_token",
#             value=f"Bearer {token}",
#             httponly=True,
#             secure=True,  # Enable in production with HTTPS
#             samesite="lax",
#             max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
#         )

#         return response

#     except Exception as e:
#         return templates.TemplateResponse(
#             "login.html",
#             {"request": request, "error": str(e)}
#         )

# @router.get("/logout")
# async def logout(response: Response):
#     response = RedirectResponse(
#         url="/auth/login-page",
#         status_code=status.HTTP_303_SEE_OTHER
#     )
#     response.delete_cookie("access_token")
#     return response



@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.password):
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Invalid credentials"}
            )

        # Create access token
        token = create_access_token(
            {"sub": user.email},
            datetime.timedelta(minutes=30)
        )

        # Create JSON response
        response = JSONResponse(
            content={
                "status": "success",
                "message": "Login successful",
                "user": {
                    "email": user.email,
                    "username": user.username
                }
            }
        )

        response = RedirectResponse(
            url="/food/food-page",  # Redirect to home page
            status_code=303  # Using 303 for POST-to-GET redirect
        )

        # Set secure cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,
            secure=True,  # Enable in production with HTTPS
            samesite="lax",
            max_age=30 * 60  # 30 minutes in seconds
        )

        return response

    except Exception as e:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": str(e)}
        )
    

@router.get("/profile")
async def get_profile(request: Request, db: Session = Depends(get_db)):
    try:
        # Get token from cookie
        token = request.cookies.get("access_token")
        if not token or not token.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"error": "Not authenticated"}
            )
        
        # Extract token value
        token = token.split(" ")[1]
        
        # Decode token
        payload = jwt.decode(
            token, 
            os.getenv("SECRET_KEY", "mysecret"), 
            algorithms=["HS256"]
        )
        
        # Get user email from token
        email = payload.get("sub")
        
        # Get user from database
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return JSONResponse(
                status_code=404,
                content={"error": "User not found"}
            )
        
        # Return user data
        return JSONResponse(
            content={
                "status": "success",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    # Add any other user fields you want to return
                    "created_at": str(user.created_at) if hasattr(user, 'created_at') else None
                }
            }
        )

    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=401,
            content={"error": "Token has expired"}
        )
    except jwt.PyJWTError:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid token"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )



@router.get("/logout")
async def logout():
    response = JSONResponse(
        content={
            "status": "success",
            "message": "Logged out successfully"
        }
    )

    response = RedirectResponse(
        url="/",
        status_code=303
    )

    
    # Clear the access token cookie
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    return response
   

@router.get("/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("access_token")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        token = token.split(" ")[1]
        payload = jwt.decode(
            token, 
            os.getenv("SECRET_KEY", "mysecret"), 
            algorithms=["HS256"]
        )
        
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")