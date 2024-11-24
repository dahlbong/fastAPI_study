from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime

class MenuBase(BaseModel):
    calories: float = Field(..., ge=0)
    sugar: float = Field(..., ge=0)
    protein: float = Field(..., ge=0)
    sodium: float = Field(..., ge=0)
    fat: float = Field(..., ge=0)
    caffeine: float = Field(..., ge=0)

class MenuCreateSchema(MenuBase):
    name: str = Field(..., min_length=1, max_length=255)

    @field_validator('name')
    def validate_name(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('이름은 공백일 수 없습니다')
        return v.strip()

class MenuUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    calories: Optional[float] = Field(None, ge=0)
    sugar: Optional[float] = Field(None, ge=0)
    protein: Optional[float] = Field(None, ge=0)
    sodium: Optional[float] = Field(None, ge=0)
    fat: Optional[float] = Field(None, ge=0)
    caffeine: Optional[float] = Field(None, ge=0)

    @field_validator('*')
    def validate_not_negative(cls, v, info):
        if v is not None and v < 0:
            raise ValueError(f'{info.field_name}는 음수일 수 없습니다')
        return v

class MenuResponseSchema(BaseModel):
    id: int
    name: str
    calories: float
    sugar: float
    protein: float
    sodium: float
    fat: float
    caffeine: float
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
