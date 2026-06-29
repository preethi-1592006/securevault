from fastapi import APIRouter
from fastapi import APIRouter, Depends 
from database import SessionLocal, engine
from models import Vault, Base
from auth import *
from schemas import VaultSchema, VaultEntry 
router = APIRouter()

@router.post("/vault", summary="Create Vault Entry")
def create_vault(data: VaultSchema, token: str = Depends(oauth2_scheme)):

    print("VAULT API CALLED")
    print("TOKEN RECEIVED:", token)
    print("DATA RECEIVED:", data)

    if not token:
        print("NO TOKEN FOUND → NOT AUTHENTICATED ERROR") 

    return {"message": "debug complete"}  
# ---------------- VAULT READ ----------------
@router.get("/vault", summary="Get All Vault Entries")
def get_vault(token: str = Depends(oauth2_scheme)):

    print("GET /vault CALLED")

    try:
        db = SessionLocal()

        print("TOKEN RECEIVED:", token)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload["sub"]

        print("USER EMAIL FROM TOKEN:", user_email)

        entries = db.query(Vault).filter(
            Vault.user_email == user_email
        ).all()

        print("DATA FROM DB:", entries)

        for e in entries:
            e.password = decrypt(e.password)

        db.close()

        return {
            "message": "Vault fetched successfully",
            "data": entries
        }

    except Exception as e:
        print("ERROR IN GET VAULT:", e)
        return {
            "error": str(e)
        } 
# ---------------- VAULT DELETE ----------------
@router.delete("/vault/{vault_id}", summary="Delete Vault Entry") 
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
@router.get("/vault/{id}")
def get_vault(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()

    vault = db.query(Vault).filter(Vault.id == id).first()

    if not vault:
        db.close()
        return {"message": "Vault entry not found"}

    db.close() 
    return vault 

@router.put("/vault/{id}", summary="Update Vault Entry") 
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

