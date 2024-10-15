import asyncio
import sys
import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ + "../../"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from warehouse_management.main import db
from warehouse_management.model.permission import PermissionModel
from warehouse_management.model.role import RoleModel
from warehouse_management.model.role_permission import RolePermissionsModel

from warehouse_management.schema.role_schema import RoleCreate
from warehouse_management.enum.permission_enum import PermissionEnum


default_roles = [{"role": "admin", "name": "Админ"}, {"role": "client", "name": "Клиент"}]


async def seed_default_roles_up():
    async with db.async_session() as async_session:
        try:
            # admin role
            result = await async_session.execute(select(PermissionModel))
            permissions = result.scalars().all()
            if not len(permissions):
                print("There are no permissions in the database. Please try \"task seed:permissions-up\" first")
                return

            result = await async_session.execute(
                select(RoleModel).where(RoleModel.role.in_([role["role"] for role in default_roles]))
            )
            roles = result.scalars().all()

            if len(roles) == len(default_roles):
                print("---------------------------")
                print(f"Warning seeding role: Data also in database!")
                return

            for role in default_roles:
                try:
                    admin_role = RoleCreate(
                        role=role["role"],
                        name=role["name"],
                    )
                    query = RoleModel(
                        **{k: v for k, v in admin_role.model_dump().items() if k != "permissions"}
                    )

                    async_session.add(query)
                    await async_session.flush()

                    if role["role"] == "admin":
                        for permission in permissions:
                            role_permission_link = RolePermissionsModel(
                                role=query.role, permission=permission.permission
                            )
                            async_session.add(role_permission_link)
                    elif role["role"] == "client":
                        client_permissions = [PermissionEnum.create_order, PermissionEnum.show_order, PermissionEnum.show_product]
                        for permission in client_permissions:
                            role_permission_link = RolePermissionsModel(
                                role=query.role, permission=permission
                            )
                            async_session.add(role_permission_link)
                except IntegrityError:
                    continue

            await async_session.commit()
            print("========================")
            print("Created 'admin' and 'client' roles and gave all permissions")
            print("Roles data seeded successfully!")

        except IntegrityError:
            print("---------------------------")
            print(f"Warning seeding roles: Data also in database!")
        except Exception as e:
            print("---------------------------")
            print(f"Error seeding up Roles: {e}")


async def seed_default_roles_down():
    async with db.async_session() as async_session:
        try:
            result = await async_session.execute(
                select(RoleModel).where(RoleModel.role.in_([role["role"] for role in default_roles]))
            )
            roles = result.scalars().all()
            for role in roles:
                await async_session.delete(role)
                await async_session.commit()

            print("========================")
            print("Removed roles and took all permissions")
        except Exception as e:
            print("---------------------------")
            print(f"Error seeding down Roles: {e}")


if __name__ == "__main__":
    import sys

    if sys.argv[-1] == "--up":
        asyncio.run(seed_default_roles_up())
    elif sys.argv[-1] == "--down":
        asyncio.run(seed_default_roles_down())
    else:
        print(
            "use --up or --down arguments when you run seeder! \n",
            "Example: 'python seeder_name.py --up' or 'python seeder_name.py --down'",
        )
