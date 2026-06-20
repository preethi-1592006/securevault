from pydantic import BaseModel

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