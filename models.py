from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    email = Column(String(100))
    password = Column(String(100)) 
class Vault(Base):
    __tablename__ = "vault"

    id = Column(Integer, primary_key=True, index=True)
    website = Column(String(100))
    username = Column(String(100))
    password = Column(String(255))
    user_email = Column(String(100))  