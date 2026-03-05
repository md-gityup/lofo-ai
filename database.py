import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
import psycopg2.pool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DATABASE_URL,
    cursor_factory=psycopg2.extras.RealDictCursor,
)


@contextmanager
def get_connection():
    conn = _pool.getconn()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)
