import unittest
from fastapi.testclient import TestClient
from dependency_injector.wiring import inject
from app.core.container import Container
from app.schema.base_schema import MessageResponseBase
from app.main import app


# Mock RoleService for testing
class MockRoleService:
    async def remove_by_attr(self, role: str) -> MessageResponseBase:
        return MessageResponseBase(message="Role deleted successfully")


# Inject the mock RoleService
@inject
def provide_mock_role_service() -> MockRoleService:
    return MockRoleService()


Container.role_service.override(provide_mock_role_service)


class TestRoleDelete(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_delete_role_success(self):
        response = self.client.delete("/roles/test_role")
        assert response.status_code == 200
        assert response.json() == {"message": "Role deleted successfully"}

    def test_delete_role_not_found(self):
        response = self.client.delete("/roles/non_existent_role")
        assert response.status_code == 404
        assert response.json() == {"detail": "Role not found"}

    def test_delete_role_invalid_role_name(self):
        response = self.client.delete("/roles/123")
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["path", "role"],
                    "msg": "str type expected",
                    "type": "type_error.str",
                }
            ]
        }

    def test_delete_role_empty_role_name(self):
        response = self.client.delete("/roles/")
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["path", "role"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }

    def test_delete_role_no_permission(self):
        response = self.client.delete(
            "/roles/test_role", headers={"Authorization": "invalid_token"}
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "Permission denied"}


if __name__ == "__main__":
    unittest.main()
