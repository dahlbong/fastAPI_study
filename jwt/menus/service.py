from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from menus.models import MenuModel
from menus.schemas import MenuCreateSchema, MenuUpdateSchema, MenuResponseSchema

def _get_menu_by_name(db: Session, menu_name: str) -> Optional[MenuModel]: # 헬퍼메서드
    return (
        db.query(MenuModel)
        .filter(
            MenuModel.name == menu_name,
            MenuModel.is_deleted == False).first()
    )

def create_menu(db: Session, menu_data: MenuCreateSchema) -> MenuResponseSchema:
    """Create a new menu item."""
    if _get_menu_by_name(db, menu_data.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 등록된 메뉴입니다."
        )

    new_item = MenuModel(**menu_data.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return MenuResponseSchema.from_orm(new_item)

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
    """Soft delete a menu item."""
    menu_item = _get_menu_by_name(db, menu_name)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    menu_item.is_deleted = True
    db.commit()
