import pytest
from fastapi import status
from app.schema.base_schema import MessageResponseBase


# Test case 1: Very long string as role parameter
@pytest.mark.asyncio
async def test_delete_very_long_role_returns_400(client, role_service_mock):
    # Arrange
    role_service_mock.remove_by_attr.return_value = None
    very_long_role = (
            "a" * 1001
    )  # 1001 characters, which is more than the maximum allowed length

    # Act
    response = await client.delete(f"/roles/{very_long_role}")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Role name should be at most 1000 characters long."
    }


# Test case 2: Role parameter is not a string
@pytest.mark.asyncio
async def test_delete_non_string_role_returns_400(client, role_service_mock):
    # Arrange
    role_service_mock.remove_by_attr.return_value = None
    non_string_role = 12345

    # Act
    response = await client.delete(f"/roles/{non_string_role}")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Role name should be a string."}


# Test case 3: Role parameter is an empty string
@pytest.mark.asyncio
async def test_delete_empty_role_returns_400(client, role_service_mock):
    # Arrange
    role_service_mock.remove_by_attr.return_value = None
    empty_role = ""

    # Act
    response = await client.delete(f"/roles/{empty_role}")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Role name should not be empty."}


# Test case 4: Role parameter is None
@pytest.mark.asyncio
async def test_delete_none_role_returns_400(client, role_service_mock):
    # Arrange
    role_service_mock.remove_by_attr.return_value = None

    # Act
    response = await client.delete("/roles/None")

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Role name should not be None."}


# Test case 5: Role parameter is a valid string
@pytest.mark.asyncio
async def test_delete_valid_role_returns_200(client, role_service_mock):
    # Arrange
    role_service_mock.remove_by_attr.return_value = MessageResponseBase(
        message="Role deleted successfully."
    )
    valid_role = "admin"

    # Act
    response = await client.delete(f"/roles/{valid_role}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Role deleted successfully."}
