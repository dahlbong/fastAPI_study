from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class MenuBase(BaseModel):
    calories: float = Field(..., ge=0)
    sugar: float = Field(..., ge=0)
    protein: float = Field(..., ge=0)
    sodium: float = Field(..., ge=0)
    fat: float = Field(..., ge=0)
    caffeine: float = Field(..., ge=0)

class MenuCreateSchema(MenuBase):
    name: str = Field(..., min_length=1, max_length=255)

class MenuUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    calories: Optional[float] = Field(None, ge=0)
    sugar: Optional[float] = Field(None, ge=0)
    protein: Optional[float] = Field(None, ge=0)
    sodium: Optional[float] = Field(None, ge=0)
    fat: Optional[float] = Field(None, ge=0)
    caffeine: Optional[float] = Field(None, ge=0)

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

    model_config = ConfigDict(from_attributes=True)
