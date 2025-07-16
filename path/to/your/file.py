from pydantic import BaseModel

class YourModel(BaseModel):
    class Config:
        orm_mode = True  # 这里使用了旧的 'orm_mode'