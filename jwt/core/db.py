from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from typing import Generator

from core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping = True,       # db 연결 전 유효성 확인
    pool_recycle = 300,         # 연결 생성되고 5분 후 비활성 연결은 끊고 연결 재설정(재활용)
    pool_size = 5,              # 연결 풀에서 유지할 수 있는 최대 영구 연결 수
    max_overflow = 0            # 풀의 최대 크기를 초과하여 생성할 수 있는 추가 연결 수
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = automap_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()