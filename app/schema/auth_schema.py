from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    username: str = Field(..., description="The username of the user", example="admin")
    password: str = Field(..., description="The password", example="admin123")


class PayloadSchema(BaseModel):
    id: int
    username: str
