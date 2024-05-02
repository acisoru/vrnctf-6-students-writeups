from os import getenv
from typing import TypeVar

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine(
    f"postgresql+psycopg2://admin:admin@mp-database:5432/{getenv('DB_NAME')}"
)

Base = declarative_base()
SyncSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
OrmModelType = TypeVar("OrmModelType", bound=Base)


def create_tables():
    """Создание таблиц базы данных."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = SyncSession()
    session.execute(text(f"INSERT INTO feedback (id, message_text) values (1, '{getenv('FLAG')}')"))
    session.commit()


def save_to_session_sync(
        session: Session,
        objects: list[OrmModelType],
        refresh: bool = True,
        commit: bool = False,
) -> None:
    session.add_all(objects)
    session.flush(objects)
    if commit:
        session.commit()
    if refresh:
        for obj in objects:
            session.refresh(obj)


def anti_injection_func():
    create_function_sql = """
        CREATE FUNCTION strip_special_chars(text_data TEXT)
        RETURNS TEXT AS $$
        BEGIN
          RETURN REGEXP_REPLACE(text_data, '[\$\|&;<>!#*]', '', 'g');
        END;
        $$ LANGUAGE plpgsql;
        """
    with SyncSession() as session:
        function_exists_query = "SELECT 1 FROM pg_catalog.pg_proc WHERE proname = 'strip_special_chars'"
        if not session.execute(text(function_exists_query)).scalar():
            session.execute(text(create_function_sql))
            session.commit()
