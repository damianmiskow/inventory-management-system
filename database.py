import sqlite3
from contextlib import contextmanager
from pathlib import Path


PROJECT_DIRECTORY = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_DIRECTORY / "database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def database_connection():
    connection = get_connection()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
