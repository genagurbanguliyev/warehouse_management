import asyncio
import sys
import os

from sqlalchemy.future import select

from app.schema.role_schema import RoleCreate

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ + "../../"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.main import db
from app.model.role import RoleModel


async def seed_user_role_up():
    async with db.async_session() as async_session:
        try:
            # Check if the 'user' role already exists
            result = await async_session.execute(
                select(RoleModel).where(RoleModel.role == "user")
            )
            user_role: RoleModel | RoleCreate = result.scalar_one_or_none()

            if not user_role:
                # Create 'user' role if it does not exist
                admin_role = RoleCreate(
                    role="user",
                    name_tm="User",
                    name_ru="Пользователь",
                )

            query = RoleModel(
                **{k: v for k, v in admin_role.model_dump().items() if k != "permissions"}
            )

            async_session.add(query)
            await async_session.commit()
            await async_session.refresh(query)
            print("========================")
            print("Created 'user' role without any permissions")
            print("User Role data seeded successfully!")
        except Exception as e:
            print("---------------------------")
            print(f"Error seeding up User Role: {e}")


async def seed_user_role_down():
    async with db.async_session() as async_session:
        try:
            result = await async_session.execute(
                select(RoleModel).where(RoleModel.role == "user")
            )
            user_role = result.scalar_one_or_none()
            if user_role:
                await async_session.delete(user_role)
                await async_session.commit()
            print("========================")
            print("Removed 'user' role")
        except Exception as e:
            print("---------------------------")
            print(f"Error seeding down User Role: {e}")


if __name__ == "__main__":
    import sys

    if sys.argv[-1] == "--up":
        asyncio.run(seed_user_role_up())
    elif sys.argv[-1] == "--down":
        asyncio.run(seed_user_role_down())
    else:
        print(
            "use --up or --down arguments when you run seeder! \n",
            "Example: 'python seeder_name.py --up' or 'python seeder_name.py --down'",
        )
