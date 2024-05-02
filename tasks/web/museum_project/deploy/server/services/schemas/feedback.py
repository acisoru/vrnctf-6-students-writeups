from pydantic import BaseModel


class Feedback(BaseModel):
    message_text: str

    class Config:
        orm_mode = True
