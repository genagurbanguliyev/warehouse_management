import os

import pytest
from httpx import AsyncClient, ASGITransport

from warehouse_management.core.config import configs
from warehouse_management.main import app
from warehouse_management.seeders.seed_default_roles import seed_default_roles_up
from warehouse_management.seeders.seed_create_database import seed_create_database_up, seed_create_database_down
from warehouse_management.seeders.seed_db_migration import seed_db_migration_up
from warehouse_management.seeders.seed_default_users import seed_default_users_up
from warehouse_management.seeders.seed_permissions import seed_permissions_up


async def reset_db():
    if "test" in configs.DATABASE_URL:
        try:
            await seed_create_database_down()
            await seed_create_database_up()
            await seed_db_migration_up()
        except Exception as err:
            raise Exception("rest_db create_database err======  ", err)
        else:
            await seed_permissions_up()
            await seed_default_roles_up()
            await seed_default_users_up()
    else:
        raise Exception("Not in test environment")


@pytest.mark.order(1)
@pytest.mark.anyio
async def test_init_db():
    db_path = "tested"
    # if not os.path.exists(db_path):
    try:
        await reset_db()
    except Exception as err:
        raise Exception("init_db->reset_db error============================  ", err)
        # else:
        #     with open(db_path, 'w') as file:
        #         file.write("Tested")
    else:
        print("Database already exists, skipping reset_db")


@pytest.fixture(scope='module')
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
