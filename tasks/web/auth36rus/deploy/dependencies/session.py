from contextlib import contextmanager

from sqlalchemy.orm import Session

from database import SyncSession


def get_sync_session() -> Session:
    with sync_session_factory() as session:
        try:
            yield session
        except Exception as exc:
            session.rollback()
            raise exc


@contextmanager
def sync_session_factory():
    session = SyncSession()
    try:
        yield session
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()
