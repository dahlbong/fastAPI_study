from sqlalchemy.ext.automap import automap_base
from core.db import engine

# 기존 테이블을 자동으로 매핑하는 Base 클래스 생성 & 테이블 구조 반영
AutomapBase = automap_base()
AutomapBase.prepare(engine, reflect=True)

# users 테이블에 대한 모델 클래스 생성
class UserModel(AutomapBase):
    __tablename__ = 'users'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'level': self.level,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'verified_at': self.verified_at,
            'registered_at': self.registered_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    @property
    def is_admin(self):
        return self.level == 'admin'
    
    @property
    def is_guest(self):
        return self.level == 'guest'