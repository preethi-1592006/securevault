from fastapi import APIRouter 
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionLocal
from models import User as DBUser
from auth import pwd_context, create_access_token, oauth2_scheme, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from schemas import RegisterUser  
router = APIRouter()     

@router.post("/register", summary="Register a new user")
def register(user: RegisterUser):

    db = SessionLocal()

    hashed_password = pwd_context.hash(user.password) 

    new_user = DBUser(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User registered successfully"}


# ---------------- LOGIN ----------------
from fastapi.security import OAuth2PasswordRequestForm 
@router.post("/login", summary="User Login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    print("LOGIN API CALLED")
    print("USERNAME:", form_data.username)
    print("PASSWORD:", form_data.password)

    token = create_access_token(
        {"sub": form_data.username}
    )

    print("TOKEN GENERATED:", token)

    return { 
        "access_token": token,
        "token_type": "bearer"
    } 

# ---------------- PROFILE (PROTECTED) ----------------
@router.get("/profile", summary="Get User Profile") 
def profile(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        ) 

        return {
            "message": "Access granted",
            "user": payload["sub"] 
        }

    except JWTError:
        return {"message": "Invalid token"} 
