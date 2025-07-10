from pydantic import BaseModel

class UserBase(BaseModel):
    full_name: str
    telegram_chat_id: int
    role: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True