from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

app = FastAPI()
# 데이터베이스 URL 설정 (PyMySQL 사용)
DATABASE_URL = "mysql+pymysql://user:secure_password@localhost:3306/starbucks_menu"

# SQLAlchemy 엔진 및 세션 설정
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base 클래스 생성
Base = declarative_base()

# 데이터베이스 모델 정의
class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    calories = Column(Float, nullable=False)
    sugar = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    sodium = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    caffeine = Column(Float, nullable=False)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# Pydantic 모델 자동 생성
MenuSchema = sqlalchemy_to_pydantic(Menu)

# ------------------------------------------------- C R U D ---------------------------------------------------------- #

# C
@app.post("/menu/", response_model=MenuSchema)
def create_menu_item(menu: MenuSchema, db: Session = Depends(get_db)):
    existing_item = db.query(Menu).filter(Menu.name == menu.name)
    if existing_item:
        raise HTTPException(status_code=400, detail="already exists")
    new_item = Menu(**menu.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# R
@app.get("/menu/{menu_name}", response_model=MenuSchema)
def read_menu(menu_name: str, db: Session = Depends(get_db)):
    menu_item = db.query(Menu).filter(Menu.name == menu_name)
    if not menu_item:
        raise HTTPException(status_code=404, detail="not found")
    return menu_item

# U
@app.put("/menu/{menu_name}", response_model=MenuSchema)
def update_menu_item(menu_name: str, updated_menu: MenuSchema, db: Session = Depends(get_db)):
    menu_item = db.query(Menu).filter(Menu.name == menu_name)
    if not menu_item:
        raise HTTPException(status_code=404, detail="not found")

    for key, value in updated_menu.dict(exclude_unset=True).items():
        setattr(menu_item, key, value)

    db.commit()
    db.refresh(menu_item)
    return menu_item

# D
@app.delete("/menu/{menu_name}", response_model=dict)
def delete_menu_item(menu_name: str, db: Session = Depends(get_db)):
    menu_item = db.query(Menu).filter(Menu.name == menu_name)
    if not menu_item:
        raise HTTPException(status_code=404, detail="not found")

    db.delete(menu_item)
    db.commit()
    return {"message": "delete success"}
