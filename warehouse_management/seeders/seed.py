import os
import sys
import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ + "../../"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from warehouse_management.main import db


async def seed_up(seeder: str, filename: str, model: Any):
    async with db.async_session() as async_session:
        # Read the JSON file
        try:
            file_path = f"warehouse_management/seeders/assets/{filename}.json"
            with open(file_path, "r", encoding="utf-8") as file:
                file_data = json.load(file)

            # Insert permissions into the database
            for data in file_data:
                data_model = model(**data)
                async_session.add(data_model)

            await async_session.commit()
            print("================================")
            print(f"{seeder} data seeded successfully!")
        except FileNotFoundError:
            print("---------------------------")
            print(f"Error seeding {seeder}: File does not exist")
        except IntegrityError:
            print("---------------------------")
            print(f"Warning seeding {seeder}: Data also in database")
        except Exception as e:
            print("---------------------------")
            print(f"Error seeding {seeder}: {e}")


async def seed_down(seeder: str, tablename: str):
    async with db.async_session() as async_session:
        stmt = text(f"TRUNCATE TABLE {tablename} CASCADE;")
        try:
            await async_session.execute(stmt)
            await async_session.commit()
            print("====================")
            print(f"{seeder} data seeded successfully!")
        except Exception as e:
            print("---------------------------")
            print(f"Error seeding {seeder}: {e}")
