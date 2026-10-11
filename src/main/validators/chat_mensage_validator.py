from pydantic import BaseModel, Field

class MensageToAIValidator(BaseModel):
    mensage: str = Field(..., min_length=1, max_length=500)
