from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from core.db import get_db
from menus.schemas import *
from menus.service import *
from users.service import get_user_level

router = APIRouter(prefix="/menu", tags=["menu"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_menu_item(menu: MenuCreateSchema, db: Session = Depends(get_db), user_level: str = Depends(get_user_level)):
    if user_level != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자 권한이 필요합니다.")
    create_menu(db, menu)
    return {"message": "메뉴 등록이 완료되었습니다."}

@router.get("/", response_model=List[MenuResponseSchema])
def list_menu_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_menu_list(db, skip, limit)

@router.get("/{menu_name}", response_model=MenuResponseSchema)
def read_menu(menu_name: str, db: Session = Depends(get_db)):
    return get_menu_by_name(db, menu_name)

@router.patch("/{menu_name}")
def update_menu_item(menu_name: str, menu_data: MenuUpdateSchema, db: Session = Depends(get_db), user_level: str = Depends(get_user_level)):
    if user_level != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자 권한이 필요합니다.")
    update_menu(db, menu_name, menu_data)
    return {"message": "업데이트가 완료되었습니다."}

@router.delete("/{menu_name}", status_code=status.HTTP_200_OK)
def delete_menu_item(menu_name: str, db: Session = Depends(get_db), user_level: str = Depends(get_user_level)):
    if user_level != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자 권한이 필요합니다.")
    delete_menu(db, menu_name)
    return {"message": "삭제가 완료되었습니다."}
