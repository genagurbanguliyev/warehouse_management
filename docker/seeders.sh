#!/bin/bash

# Run database migrations and seeders (if applicable)
python /fastapi_app/warehouse_management/seeders/seed_create_database.py --up
alembic upgrade head
python /fastapi_app/warehouse_management/seeders/seed_permissions.py --up
python /fastapi_app/warehouse_management/seeders/seed_default_roles.py --up
python /fastapi_app/warehouse_management/seeders/seed_default_users.py --up
