from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies.session import get_sync_session
from api.schemas.feedback import Feedback
from services.feedback.create_feedback_command import (
    CreateFeedbackCommand,
    CreateFeedbackCommandError,
    WAFTimeoutError
)

feedback_router = APIRouter(
    tags=["feedback"]
)


@feedback_router.post("/send")
async def send_feedback(
    feedback: Feedback, session: Session = Depends(get_sync_session)
):
    command = CreateFeedbackCommand(session, feedback)
    try:
        message_text = await command.execute()
    except CreateFeedbackCommandError as exc:
        raise HTTPException(status_code=400) from exc
    except WAFTimeoutError as exc:
        raise HTTPException(418) from exc

    return {"message_text": message_text}
