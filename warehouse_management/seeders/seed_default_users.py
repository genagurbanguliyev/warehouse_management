import asyncio
import sys
import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ + "../../"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from warehouse_management.core.config import configs, environment
from warehouse_management.main import db
from warehouse_management.model.user import UserModel
from warehouse_management.model.role import RoleModel
from warehouse_management.core.password import get_password_hash

from warehouse_management.seeders.seed_default_roles import default_roles


async def seed_default_users_up():
    async with db.async_session() as async_session:
        try:
            password_hash = get_password_hash(configs.DEFAULT_ADMIN_PASSWORD)
            result = await async_session.execute(
                select(RoleModel).where(RoleModel.role.in_([role["role"] for role in default_roles]))
            )
            roles = result.scalars().all()

            if len(roles) != len(default_roles):
                print("---------------------------")
                print(f"Warning seeding default_users: admin or client role is not in roles!")
                return

            for role in default_roles:
                try:
                    if role["role"] == "admin":
                        default_admin = UserModel(
                            name="Default admin",
                            username=configs.DEFAULT_ADMIN,
                            password=password_hash,
                            role="admin",
                        )

                        async_session.add(default_admin)
                    elif role["role"] == "client" and environment == "test":
                        default_client = UserModel(
                            name="Default client",
                            username="client",
                            password="client",
                            role="client"
                        )
                        async_session.add(default_client)
                except IntegrityError:
                    continue

            await async_session.commit()
            print("====================")
            print("Create Default users")
            print("Seeder run Successfully!")
        except IntegrityError:
            print("---------------------------")
            print(f"Warning seeding default_users: Data also in database!")
        except Exception as e:
            print("---------------------------")
            print(f"Error seeding up Default users: {e}")


async def seed_default_users_down():
    async with db.async_session() as async_session:
        try:
            result = await async_session.execute(
                select(UserModel)
                .where(UserModel.username.in_(["admin", "client"]))
            )
            users = result.scalars().all()
            if len(users):
                for user in users:
                    await async_session.delete(user)
                    await async_session.commit()
            else:
                print("Users already doesn't exist")
            print("====================")
            print("Delete Default users")
            print("Seeder run Successfully!")
        except Exception as e:
            print("---------------------------")
            return f"Error seeding down Default users: {e}"


if __name__ == "__main__":
    import sys

    if sys.argv[-1] == "--up":
        asyncio.run(seed_default_users_up())
    elif sys.argv[-1] == "--down":
        asyncio.run(seed_default_users_down())
    else:
        print(
            "use --up or --down arguments when you run seeder! \n",
            "Example: 'python seeder_name.py --up' or 'python seeder_name.py --down'",
        )
