from sqlalchemy import Integer, Column, String, DateTime

from database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    message_text = Column(String, nullable=False)
