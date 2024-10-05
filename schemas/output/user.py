from typing import List

from pydantic import BaseModel


class BaseUserDisplay(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool

    class Config:
        from_attributes = True


class BaseUserAll(BaseModel):
    users: List[BaseUserDisplay]

    class Config:
        from_attributes = True
