import asyncio
import sys
import os

from psycopg.errors import DuplicateDatabase
from sqlalchemy import text, create_engine
from sqlalchemy.exc import ProgrammingError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ + "../../"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.core.config import configs
import app.model  # noqa

DATABASE_URL = f"postgresql+psycopg://{configs.DB_USER}:{configs.DB_PASS}@{configs.DB_HOST}:{configs.DB_PORT}/postgres"


async def seed_create_database_up():
    # Step 1: Create the Database
    engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        try:
            conn.execute(text(f"CREATE DATABASE {configs.DB_NAME}"))
            print("Created database successfully!!!")
        except DuplicateDatabase:
            print("Warning: Database already exists!")
        except ProgrammingError as e:
            print(f"Database creation error: {e}")


async def seed_create_database_down():
    engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        try:
            conn.execute(text(f"DROP DATABASE IF EXISTS {configs.DB_NAME}"))
            print("Deleted database successfully!!!")
        except ProgrammingError as e:
            print(f"Database deletion error: {e}")


if __name__ == "__main__":
    import sys

    if sys.argv[-1] == "--up":
        asyncio.run(seed_create_database_up())
    elif sys.argv[-1] == "--down":
        asyncio.run(seed_create_database_down())
    else:
        print(
            "use --up or --down arguments when you run seeder! \n",
            "Example: 'python seeder_name.py --up' or 'python seeder_name.py --down'",
        )
