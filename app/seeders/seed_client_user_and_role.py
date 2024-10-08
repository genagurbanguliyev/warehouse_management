import sys
import os

from sqlalchemy.future import select

from app.enum.permission_enum import PermissionEnum
from app.model import RolePermissionsModel, PermissionModel
from app.schema.role_schema import RoleCreate

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ + "../../"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.core.config import environment
from app.main import db
from app.model.user import UserModel
from app.model.role import RoleModel


async def seed_client_user_and_role_for_test_up():
    print(f"envvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv {environment}")
    if environment == "test":
        async with db.async_session() as async_session:
            try:
                result = await async_session.execute(select(PermissionModel))
                permissions = result.scalars().all()
                if not len(permissions):
                    print("There are no permissions in the database. Please try \"task seed:permissions-up\" first")
                    return
                client_result = await async_session.execute(
                    select(RoleModel)
                    .where(RoleModel.role == "client")
                )
                client_role = client_result.scalar_one_or_none()
                if client_role is None:
                    client_role = RoleCreate(
                        role="client",
                        name="Client"
                    )
                    query = RoleModel(
                        **{k: v for k, v in client_role.model_dump().items() if k != "permissions"}
                    )

                    async_session.add(query)
                    await async_session.flush()

                for permission in permissions:
                    if permission.permission in [PermissionEnum.create_order, PermissionEnum.show_order, PermissionEnum.show_product]:
                        role_permission_link = RolePermissionsModel(
                            role=query.role, permission=permission.permission
                        )
                        async_session.add(role_permission_link)
                default_client = UserModel(
                    name="Default client",
                    username="client",
                    password="client",
                    role=client_role.role,
                    role_detail=client_role,
                )
                async_session.add(default_client)
                await async_session.commit()
                print("====================")
                print("Create Default client user")
                print("Seeder run Successfully!")
            except Exception as e:
                print("---------------------------")
                print(f"Error seeding up Default test client user: {e}")


# async def seed_client_user_and_role_for_test_down():
#     if environment == "test":
#         async with db.async_session() as async_session:
#             try:
#                 result = await async_session.execute(
#                     select(UserModel).where(UserModel.role == "client")
#                 )
#                 users = result.scalars().all()
#                 if len(users):
#                     for user in users:
#                         await async_session.delete(user)
#                         await async_session.commit()
#                 else:
#                     print("Users already doesn't exist")
#                 print("====================")
#                 print("Delete Default client role client")
#                 print("Seeder run Successfully!")
#             except Exception as e:
#                 print("---------------------------")
#                 return f"Error seeding down Default client: {e}"
#
#
# if __name__ == "__main__":
#     import sys
#
#     if sys.argv[-1] == "--up":
#         asyncio.run(seed_client_user_and_role_for_test_up())
#     elif sys.argv[-1] == "--down":
#         asyncio.run(seed_client_user_and_role_for_test_down())
#     else:
#         print(
#             "use --up or --down arguments when you run seeder! \n",
#             "Example: 'python seeder_name.py --up' or 'python seeder_name.py --down'",
#         )
