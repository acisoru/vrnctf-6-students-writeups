import time

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from services import User


def slow_equals(a, b):
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
        time.sleep(1)
    return result == 0


class UserNotFoundError(Exception):
    """Пользователь не найден"""


class ReadUserQuery:
    def __init__(self, session: Session, user: User | None = None):
        self.session = session
        self.user = user

    def get(self):
        query = select(models.User).where(models.User.login == self.user.login)
        found_user = self.session.execute(query).scalar()
        if not found_user:
            raise UserNotFoundError

        if not slow_equals(found_user.password, self.user.password):
            raise UserNotFoundError

        return User.from_orm(found_user)

    def get_by_id(self, user_id: int):
        query = select(models.User).where(
            models.User.id == user_id,
        )
        user = self.session.execute(query).scalar()
        if not user:
            raise UserNotFoundError

        return User.from_orm(user)
