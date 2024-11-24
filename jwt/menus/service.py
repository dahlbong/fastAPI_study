from sqlalchemy.orm import Session
from sqlalchemy import exists
from fastapi import HTTPException, status
from typing import List

from menus.models import MenuModel
from menus.schemas import MenuCreateSchema, MenuUpdateSchema, MenuResponseSchema

def _menu_exists(db: Session, menu_name: str) -> bool:  # 헬퍼메서드
    return db.query(exists().where(
        MenuModel.name == menu_name,
        MenuModel.is_deleted == False
    )).scalar()

def create_menu(db: Session, menu_data: MenuCreateSchema) -> None:
    if _menu_exists(db, menu_data.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 등록된 메뉴입니다."
        )

    new_item = MenuModel(**menu_data.dict())
    db.add(new_item)
    db.commit()

def get_menu_list(db: Session, skip: int = 0, limit: int = 100) -> List[MenuResponseSchema]:
    """Retrieve a list of menu items."""
    menu_items = (
        db.query(MenuModel)
        .filter(MenuModel.is_deleted == False)
        .order_by(MenuModel.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [MenuResponseSchema.from_orm(item) for item in menu_items]

def get_menu_by_name(db: Session, menu_name: str) -> MenuResponseSchema:
    """Retrieve a single menu item by name."""
    menu_item = _get_menu_by_name(db, menu_name)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return MenuResponseSchema.from_orm(menu_item)

def update_menu(db: Session, menu_name: str, menu_data: MenuUpdateSchema) -> MenuResponseSchema:
    """Update a menu item."""
    menu_item = _get_menu_by_name(db, menu_name)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    for key, value in menu_data.dict(exclude_unset=True).items():
        setattr(menu_item, key, value)

    db.commit()
    db.refresh(menu_item)

    return MenuResponseSchema.from_orm(menu_item)

def delete_menu(db: Session, menu_name: str) -> None:
    menu_item = _get_menu_by_name(db, menu_name)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    menu_item.is_deleted = True
    db.commit()
