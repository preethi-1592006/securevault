SecureVault API

Features

- User Registration
- User Login with JWT Authentication
- User Profile Endpoint
- Vault CRUD Operations
- Password Encryption & Decryption
- Password Hashing using bcrypt
- FixedSizeStack Data Structure

Technologies Used

- Python 
- FastAPI
- MySQL
- SQLAlchemy
- JWT Authentication
- Passlib
- bcrypt
- Pydantic

Installation

1. Clone the repository

```bash
git clone <repository_url>
```

2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Run the server

```bash
uvicorn main:app --reload
```

---

API Endpoints

Authentication

- POST `/register`
- POST `/login`
- GET `/profile`

Vault

- GET `/vault`
- POST `/vault`
- GET `/vault/{id}`
- PUT `/vault/{id}`
- DELETE `/vault/{vault_id}`

Authentication

This project uses **JWT Bearer Token Authentication**.

1. Register a user.
2. Login to receive an Access Token.
3. Click **Authorize** in Swagger UI.
4. Enter the JWT token.
5. Access protected APIs.

Data Structure Used

- FixedSizeStack implemented using a Python class.

API Documentation

After running the project, open:

```
http://127.0.0.1:8000/docs
```

to access the interactive Swagger API documentation.

Project Structure

```
securevault/
│
├── routers/
│   ├── auth.py
│   └── vault.py
│
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── main.py
├── requirements.txt 
├── README.md
└── .env
``` 