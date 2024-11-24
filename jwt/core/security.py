from passlib.context import CryptContext    #비밀번호 해시 및 검증 관련 알고리즘 지원 라이브러리
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from fastapi import Depends, HTTPException, status

from core.db import get_db
from users.models import UserModel
from core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   # CryptContext 객체 생성
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def create_access_token(data, expiry: timedelta):
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

async def create_refresh_token(data, expiry: timedelta):
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
    except JWTError:
        return None
    return payload

def get_current_user(token: str = Depends(oauth2_scheme), db = None):
    payload = get_token_payload(token)
    if not payload or type(payload) is not dict:
        return None
    
    user_id = payload.get('id', None)
    if not user_id:
        return None
    
    if not db:
        db = next(get_db())

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return user

class JWTAuth:
    async def authenticate(self, conn):
        guest = AuthCredentials({'unauthenticated'}), UnauthenticatedUser()

        if 'authorization' not in conn.headers:
            return guest
        token = conn.headers.get('authorization').split(' ')[1]   #Bearer token_hash
        if not token:
            return guest
        user = get_current_user(token=token)

        if not user:
            return guest
        
        return AuthCredentials('Authenticated'), user