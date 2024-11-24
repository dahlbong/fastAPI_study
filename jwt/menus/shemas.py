from pydantic import BaseModel

class CreateMenu(BaseModel):
    name: str
    calories: float
    sugar: float
    protein: float
    sodium: float
    fat: float
    caffeine: float