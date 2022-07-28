from typing import Optional, List
from pydantic import BaseModel


class Prediction(BaseModel):
    x_predict: Optional[List] = []

    class Config:
        schema_extra = {
            "example": {
                "x_predict": [4, 8, 10, 12, 15, 20]
            }
        }
