from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from core.db import Base, engine

# 기존 테이블을 자동으로 매핑하는 Base 클래스 생성
AutomapBase = automap_base()

# 데이터베이스의 테이블 구조를 반영
AutomapBase.prepare(engine, reflect=True)

# menu 테이블에 대한 모델 클래스 생성
class MenuModel(AutomapBase):
    __tablename__ = 'menu'
    
    # 필요한 경우 추가적인 메서드나 프로퍼티를 정의할 수 있습니다
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'calories': self.calories,
            'sugar': self.sugar,
            'protein': self.protein,
            'sodium': self.sodium,
            'fat': self.fat,
            'caffeine': self.caffeine
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)