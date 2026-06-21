SecureVault API

Features

- User Registration
- User Login with JWT Authentication
- Profile Endpoint
- Vault CRUD Operations
- Password Hashing using bcrypt
- FixedSizeStack Data Structure

Installation

1. Clone the repository
2. Create virtual environment

python -m venv venv

3. Activate virtual environment

venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Run the server

uvicorn main:app --reload

API Endpoints

- POST /register
- POST /login
- GET /profile
- GET /vault
- POST /vault
- DELETE /vault/{vault_id}

Authentication

JWT Bearer Token Authentication

Data Structure Used

FixedSizeStack implemented using Python class.

Documentation

Open:

http://127.0.0.1:8000/docs 