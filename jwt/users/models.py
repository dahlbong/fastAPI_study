from core.db import engine, Base

# 테이블 구조 반영
Base.prepare(engine, reflect=True)

# users 테이블에 대한 모델 클래스 생성
if "users" in Base.classes:
    UserModel = Base.classes.users  # "users" 테이블과 매핑
else:
    raise ValueError("users 테이블이 데이터베이스에 없습니다.")