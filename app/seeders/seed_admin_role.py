import asyncio
import sys
import os

from sqlalchemy.future import select


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ + "../../"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.main import db
from app.model.permission import PermissionModel
from app.model.role import RoleModel
from app.model.role_permission import RolePermissionsModel

from app.schema.role_schema import RoleCreate


async def seed_admin_role_up():
    async with db.async_session() as async_session:
        try:
            result = await async_session.execute(select(PermissionModel))
            permissions = result.scalars().all()
            if not len(permissions):
                print("There are no permissions in the database. Please try \"task seed:permissions-up\" first")
                return

            result = await async_session.execute(
                select(RoleModel).where(RoleModel.role == "admin")
            )
            admin_role = result.scalar_one_or_none()

            if admin_role is None:
                admin_role = RoleCreate(
                    role="admin",
                    name="Админ"
                )
                query = RoleModel(
                    **{k: v for k, v in admin_role.model_dump().items() if k != "permissions"}
                )

                async_session.add(query)
                await async_session.flush()

            for permission in permissions:
                role_permission_link = RolePermissionsModel(
                    role=query.role, permission=permission.permission
                )
                async_session.add(role_permission_link)

            await async_session.commit()
            await async_session.refresh(query)
            print("========================")
            print("Created 'admin' role and gave all permissions")
            print("Admin Role data seeded successfully!")
        except Exception as e:
            print("---------------------------")
            print(f"Error seeding up Admin Role: {e}")


async def seed_admin_role_down():
    async with db.async_session() as async_session:
        try:
            result = await async_session.execute(
                select(RoleModel).where(RoleModel.role == "admin")
            )
            admin_role = result.scalar_one_or_none()
            if admin_role:
                await async_session.delete(admin_role)
                await async_session.commit()

            print("========================")
            print("Removed 'admin' role and took all permissions")
        except Exception as e:
            print("---------------------------")
            print(f"Error seeding down Admin Role: {e}")


if __name__ == "__main__":
    import sys

    if sys.argv[-1] == "--up":
        asyncio.run(seed_admin_role_up())
    elif sys.argv[-1] == "--down":
        asyncio.run(seed_admin_role_down())
    else:
        print(
            "use --up or --down arguments when you run seeder! \n",
            "Example: 'python seeder_name.py --up' or 'python seeder_name.py --down'",
        )
