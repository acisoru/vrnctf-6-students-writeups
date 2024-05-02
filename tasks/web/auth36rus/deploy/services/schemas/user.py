from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    login: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True
