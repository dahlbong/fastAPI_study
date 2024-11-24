from sqlalchemy.orm import Session
from sqlalchemy import exists
from fastapi import HTTPException, status
from typing import List

from menus.models import MenuModel
from menus.schemas import MenuCreateSchema, MenuUpdateSchema, MenuResponseSchema


def create_menu(db: Session, menu_data: MenuCreateSchema) -> None:
    is_existing = db.query(exists().where(MenuModel.name == menu_data.name, MenuModel.is_deleted == False))
    if is_existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 등록된 메뉴입니다.")
    new_item = MenuModel(**menu_data.dict())
    db.add(new_item)
    db.commit()

def get_menu_list(db: Session, skip: int = 0, limit: int = 100) -> List[MenuResponseSchema]:
    menu_items = (
        db.query(MenuModel).filter(MenuModel.is_deleted == False).offset(skip).limit(limit).all()
    )
    return [MenuResponseSchema.from_orm(item) for item in menu_items]

def get_menu_by_name(db: Session, menu_name: str) -> MenuResponseSchema:
    menu_item = db.query(MenuModel).filter(MenuModel.name == menu_name)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="등록되지 않은 메뉴입니다."
        )
    return MenuResponseSchema.from_orm(menu_item)

def update_menu(db: Session, menu_name: str, menu_data: MenuUpdateSchema) -> None:
    menu_item = db.query(MenuModel).filter(MenuModel.name == menu_name)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="등록되지 않은 메뉴입니다."
        )
    # 업데이트할 데이터만 필터링
    fields_to_update = ['name', 'calories', 'sugar', 'protein', 'sodium', 'fat', 'caffeine']
    update_data = {
        key: value
        for key, value in menu_data.dict(exclude_unset=True).items()
        if key in fields_to_update
    }
    # 한 번에 업데이트 수행
    db.query(MenuModel).filter(MenuModel.name == menu_name).update(update_data)
    db.commit()


def delete_menu(db: Session, menu_name: str) -> None:
    menu_item = db.query(MenuModel).filter(MenuModel.name == menu_name)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    menu_item.is_deleted = True
    db.commit()
