from fastapi import FastAPI
from dotenv import load_dotenv

from routers.auth import router as auth_router
from routers.vault import router as vault_router 

load_dotenv()

app = FastAPI(
    title="SecureVault API", 
    description="Password Manager Backend using FastAPI",
    version="1.0.0"
) 

# Home API
@app.get("/")
def home():
    return {
        "message": "Hello SecureVault"
    }

# Register all routers
app.include_router(auth_router)
app.include_router(vault_router)





