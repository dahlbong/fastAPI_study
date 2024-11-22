import os                                   # 운영체제와 상호작용 (파일 경로 확인, 디렉토리 생성 및 삭제)
from pathlib import Path                    # 파일 시스템 경로를 객체지향적으로 다룰 수 있게 해줌
from dotenv import load_dotenv              # 파일에 정의된 환경변수를 app의 환경변수로 로드
from pydantic_settings import BaseSettings  # 데이터 검증 & 변환
from urllib.parse import quote_plus         # URL 인코딩


env_path = Path(".")/".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    #db
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: str = os.getenv('DB_PORT')
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    #jwt
    JWT_SECRET: str = os.getenv('JWT_SECRET')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES')

def get_settings() -> Settings:
    return Settings()   # Settings 클래스 호출하여 새로운 객체 생성하여 반환