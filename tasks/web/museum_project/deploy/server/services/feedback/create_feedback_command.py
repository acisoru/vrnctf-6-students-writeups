from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
from services.schemas.feedback import Feedback


class CreateFeedbackCommandError(Exception):
    """Невозможно создать фидбек"""


class WAFTimeoutError(Exception):
    """WAF превысил время выполнения"""


class CreateFeedbackCommand:
    def __init__(self, session: Session, feedback: Feedback):
        self.session = session
        self.feedback = feedback

    async def execute(self):
        feedback = models.Feedback(message_text=self.feedback.message_text)
        try:
            self.session.add(feedback)
            self.session.commit()
        except IntegrityError as exc:
            raise CreateFeedbackCommandError from exc

        query = f"""
                SELECT message_text FROM feedback WHERE message_text = '{self.feedback.message_text}'
            """
        message_text = self.session.execute(text(query)).fetchall()
        feedbacks = []
        for inner in message_text:
            for msg in inner:
                feedbacks.append(msg)
        return feedbacks
