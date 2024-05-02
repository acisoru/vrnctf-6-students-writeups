from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies.session import get_sync_session
from schemas.user import User
from services.user.read_user_query import ReadUserQuery, UserNotFoundError

auth_router = APIRouter(
    tags=["auth"]
)


@auth_router.post("/login")
async def login_user(user: User, session: Session = Depends(get_sync_session)) -> User:
    query = ReadUserQuery(session, user)
    try:
        user = query.get()
    except UserNotFoundError as exc:
        raise HTTPException(status_code=404) from exc

    return user
