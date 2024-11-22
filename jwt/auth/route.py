from fastapi import APIRouter, status, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.db import get_db
from auth.service import get_token, get_refresh_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description":"Not Found"}}
)


@router.post("/token", status_code=status.HTTP_200_OK)
async def auth_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await get_token(data=data, db=db)

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    return await get_refresh_token(token=refresh_token, db=db)