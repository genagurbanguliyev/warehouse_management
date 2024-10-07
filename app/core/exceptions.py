from typing import Any, Dict

from fastapi import status as fast_status
from fastapi import HTTPException


class DublicatedError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, Any] | None = None
    ) -> None:
        super().__init__(fast_status.HTTP_409_CONFLICT, detail, headers)


class AuthError(HTTPException):
    def __init__(
        self,
        status: Any = fast_status.HTTP_403_FORBIDDEN,
        detail: Any = None,
        headers: Dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status, detail, headers)


class NotFoundError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, Any] | None = None
    ) -> None:
        super().__init__(fast_status.HTTP_404_NOT_FOUND, detail, headers)


class ValidationError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, Any] | None = None
    ) -> None:
        super().__init__(fast_status.HTTP_422_UNPROCESSABLE_ENTITY, detail, headers)


class InternalError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, Any] | None = None
    ) -> None:
        super().__init__(fast_status.HTTP_500_INTERNAL_SERVER_ERROR, detail, headers)
