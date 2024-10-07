import asyncio
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ + "../../"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.seeders.seed import seed_up, seed_down
from app.model.permission import PermissionModel


async def seed_permissions_up():
    await seed_up(seeder="Permission", filename="permissions", model=PermissionModel)


async def seed_permissions_down():
    await seed_down(seeder="Permission", tablename="permissions")


if __name__ == "__main__":
    import sys

    if sys.argv[-1] == "--up":
        asyncio.run(seed_permissions_up())
    elif sys.argv[-1] == "--down":
        asyncio.run(seed_permissions_down())
    else:
        print(
            "use --up or --down arguments when you run seeder! \n",
            "Example: 'python seeder_name.py --up' or 'python seeder_name.py --down'",
        )
