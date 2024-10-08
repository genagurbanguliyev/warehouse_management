import asyncio
import os

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient

from app.core.config import configs
from app.main import app
from app.seeders.seed_admin_role import seed_admin_role_up
from app.seeders.seed_create_database import seed_create_database_up
from app.seeders.seed_db_migration import seed_db_migration_up
from app.seeders.seed_default_users import seed_default_users_up
from app.seeders.seed_permissions import seed_permissions_up
from app.seeders.seed_client_user_and_role import seed_client_user_and_role_for_test_up


async def reset_db():
    if "test" in configs.DATABASE_URL:
        try:
            await seed_create_database_up()
            await seed_db_migration_up()
        except Exception as err:
            raise Exception("rest_db create_database err======  ", err)
        else:
            await seed_permissions_up()
            await seed_admin_role_up()
            await seed_default_users_up()
            await seed_client_user_and_role_for_test_up()
    else:
        raise Exception("Not in test environment")


@pytest.fixture(scope="function", autouse=True)
async def init_db():
    db_path = "tested"
    if not os.path.exists(db_path):
        try:
            await reset_db()
        except Exception as err:
            raise Exception("init_db->reset_db error============================  ", err)
        else:
            with open(db_path, 'w') as file:
                file.write("Tested")
    else:
        print("Database already exists, skipping reset_db")


@pytest.fixture(scope="function")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# @pytest.fixture()
# def test_name(request):
#     return request.node.name
