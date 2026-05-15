from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "change_this_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


fake_users_db = {
    "engineering_user": {
        "username": "engineering_user",
        "password": "eng123",
        "role": "engineering"
    },
    "marketing_user": {
        "username": "marketing_user",
        "password": "marketing123",
        "role": "marketing"
    },
    "hr_user": {
        "username": "hr_user",
        "password": "hr123",
        "role": "hr"
    },
    "finance_user": {
        "username": "finance_user",
        "password": "finance123",
        "role": "finance"
    },
    "general_user": {
        "username": "general_user",
        "password": "general123",
        "role": "general"
    },
    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "admin"
    }
}


def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)

    if not user:
        return None

    if user["password"] != password:
        return None

    return user


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {
            "username": username,
            "role": role
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")