from auth import encrypt, decrypt 
from fastapi import FastAPI, Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from database import SessionLocal, engine
from models import Base, User as DBUser, Vault
from auth import (
    pwd_context,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme,
    create_access_token
)

load_dotenv()

app = FastAPI() 

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "Hello SecureVault"}


# ---------------- MODELS ----------------
class User(BaseModel):
    username: str
    email: str


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str


class LoginUser(BaseModel):
    email: str
    password: str


class VaultEntry(BaseModel):
    website: str
    username: str
    password: str


# ---------------- REGISTER ----------------
@app.post("/register")
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
@app.post("/login")
def login(user: LoginUser):

    db = SessionLocal()

    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()

    if not db_user:
        return {"message": "Invalid email"}

    if not pwd_context.verify(user.password, db_user.password):
        return {"message": "Invalid password"}

    token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ---------------- PROFILE (PROTECTED) ----------------
@app.get("/profile")
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


# ---------------- VAULT CREATE ----------------
@app.post("/vault")
def create_vault(entry: VaultEntry, token: str = Depends(oauth2_scheme)):

    db = SessionLocal()

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_email = payload["sub"]

    new_entry = Vault(
        website=entry.website,
        username=entry.username,
        password=encrypt(entry.password),   # 🔐 ENCRYPTED
        user_email=user_email
    )

    db.add(new_entry)
    db.commit()
    db.close()  

    return {
        "message": "Vault entry created successfully",
        "status": "success"
    } 
# ---------------- VAULT READ ----------------
@app.get("/vault")
def get_vault(token: str = Depends(oauth2_scheme)):  

    db = SessionLocal()

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_email = payload["sub"]

    entries = db.query(Vault).filter(
        Vault.user_email == user_email
    ).all()

    for e in entries:
        e.password = decrypt(e.password)

    db.close()

    return {
        "message": "Vault fetched successfully",
        "data": entries
    } 


# ---------------- VAULT DELETE ----------------
@app.delete("/vault/{vault_id}")
def delete_vault(vault_id: int):

    db = SessionLocal()

    vault = db.query(Vault).filter(Vault.id == vault_id).first()

    if not vault:
        return {"message": "Vault entry not found"}

    db.delete(vault)
    db.commit()
    db.close()

    return {"message": "Vault entry deleted successfully"}


# ---------------- DATABASE INIT ----------------
Base.metadata.create_all(bind=engine) 
@app.get("/vault/{id}")
def get_vault(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()

    vault = db.query(Vault).filter(Vault.id == id).first()

    if not vault:
        db.close()
        return {"message": "Vault entry not found"}

    db.close()
    return vault
@app.put("/vault/{id}")
def update_vault(id: int, entry: VaultEntry, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()

    vault = db.query(Vault).filter(Vault.id == id).first()

    if not vault:
        db.close()
        return {"message": "Vault entry not found"}

    vault.website = entry.website
    vault.username = entry.username
    vault.password = encrypt(entry.password)

    db.commit()
    db.refresh(vault)

    db.close()

    return {
        "message": "Vault updated successfully"
    } 







