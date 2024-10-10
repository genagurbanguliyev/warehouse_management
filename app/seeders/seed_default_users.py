import asyncio
import sys
import os

from sqlalchemy.future import select

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ + "../../"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.core.config import configs
from app.main import db
from app.model.user import UserModel
from app.model.role import RoleModel
from app.core.password import get_password_hash


async def seed_default_users_up():
    async with db.async_session() as async_session:
        try:
            password_hash = get_password_hash(configs.DEFAULT_ADMIN_PASSWORD)
            result = await async_session.execute(
                select(RoleModel)
                .where(RoleModel.role == "admin")
            )
            admin_role = result.scalar_one_or_none()
            if admin_role:
                default_admin = UserModel(
                    name="Default admin",
                    username=configs.DEFAULT_ADMIN,
                    password=password_hash,
                    role=admin_role.role,
                )

                async_session.add(default_admin)
                await async_session.commit()
                print("====================")
                print("Create Default admin")
                print("Seeder run Successfully!")
            else:
                print("---------------------------")
                print("Admin role doesn't exist")
        except Exception as e:
            print("---------------------------")
            print(f"Error seeding up Default admin: {e}")


async def seed_default_users_down():
    async with db.async_session() as async_session:
        try:
            result = await async_session.execute(
                select(UserModel).where(UserModel.role == "admin")
            )
            users = result.scalars().all()
            if len(users):
                for user in users:
                    await async_session.delete(user)
                    await async_session.commit()
            else:
                print("Users already doesn't exist")
            print("====================")
            print("Delete Default admin role user")
            print("Seeder run Successfully!")
        except Exception as e:
            print("---------------------------")
            return f"Error seeding down Default admin: {e}"


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
