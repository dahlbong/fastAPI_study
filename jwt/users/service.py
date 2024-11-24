from users.models import UserModel
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from datetime import datetime

from core.security import get_password_hash, get_current_user

async def create_user_account(data, db):
    existing_user = db.query(UserModel).filter((UserModel.email == data.email) | (UserModel.username == data.username)).first()
    if existing_user:
        if existing_user.email == data.email:
            raise HTTPException(status_code=422, detail="이미 가입한 회원입니다.")
        else:
            raise HTTPException(status_code=422, detail="이미 사용 중인 id입니다. 다른 id를 입력해주세요.")

    new_user = UserModel(
        username = data.username,
        email = data.email,
        password = get_password_hash(data.password),
        is_verified = False,
        registered_at = datetime.now()        
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_level(current_user: UserModel = Depends(get_current_user)) -> str:
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자 권한이 필요합니다.")
    return current_user.level