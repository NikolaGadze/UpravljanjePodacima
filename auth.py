from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import crud
import schemas
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from session_manager import session_manager
from database import get_db

SECRET_KEY = "09d85f74c5a23f45a8a96d8e789f72c5c0a4b4ff441b31493e809e8b762e824d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user(db, email)
    if not user or not verify_password(password, user.Password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = session_manager.get_user_id(token)
        if not token_data:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_patient(current_user: schemas.Patient = Depends(get_current_user)):
    if not hasattr(current_user, 'PatientID'):
        raise HTTPException(status_code=400, detail="Not a patient")
    return current_user

async def get_current_doctor(current_user: schemas.Doctor = Depends(get_current_user)):
    if not hasattr(current_user, 'DoctorID'):
        raise HTTPException(status_code=400, detail="Not a doctor")
    return current_user
