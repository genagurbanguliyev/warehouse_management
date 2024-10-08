import asyncio
import sys
import os

from sqlalchemy import text, create_engine
from sqlalchemy.exc import ProgrammingError


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ + "../../"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.model.base_model import Base
from app.core.config import configs
import app.model  # noqa


async def seed_db_migration_up():
    # Migrate Models
    try:
        migration_engine = create_engine(configs.DATABASE_URL, echo=False)
        Base.metadata.create_all(migration_engine)
        print("Migrate all tables successfully!!!")
    except ProgrammingError as e:
        print(f"Database migration error: {e}")


async def seed_db_migration_down():
    engine = create_engine(configs.DATABASE_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        try:
            db_query = f"""
            DO $$ DECLARE 
                r RECORD; 
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
            """
            conn.execute(text(db_query))
            print("All tables of db deleted successfully!!!")
        except ProgrammingError as e:
            print(f"Delete database tables error: {e}")


if __name__ == "__main__":
    import sys

    if sys.argv[-1] == "--up":
        asyncio.run(seed_db_migration_up())
    elif sys.argv[-1] == "--down":
        asyncio.run(seed_db_migration_down())
    else:
        print(
            "use --up or --down arguments when you run seeder! \n",
            "Example: 'python seeder_name.py --up' or 'python seeder_name.py --down'",
        )
