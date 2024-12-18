from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re

from app.utils.nickname_gen import generate_nickname


class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


def validate_url(url: Optional[str]) -> Optional[str]:
    """Validate that the URL is properly formatted."""
    if url is None:
        return url
    url_regex = r"^https?:\/\/[^\s/$.?#].[^\s]*$"
    if not re.match(url_regex, url):
        raise ValueError("Invalid URL format")
    return url


def validate_password(value: str) -> str:
    """Ensure password contains required character types."""
    requirements = {
        "lowercase letter": any(c.islower() for c in value),
        "uppercase letter": any(c.isupper() for c in value),
        "special character": any(c in "!@#$%^&*()_+-=[]{}|;':\",.<>?/`~" for c in value),
        "numeric digit": any(c.isdigit() for c in value)
    }
    for description, passed in requirements.items():
        if not passed:
            raise ValueError(f"Password must contain at least one {description}.")
    return value


class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r"^[\w-]+$", example="slime_jim12")
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] = Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")

    _validate_urls = validator(
        "profile_picture_url", "linkedin_profile_url", "github_profile_url", pre=True, allow_reuse=True
    )(validate_url)

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="Secure*1234")

    _validate_password = validator("password", pre=True, allow_reuse=True)(validate_password)


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None

    @root_validator(pre=True)
    def validate_fields(cls, values):
        if not any(values.get(field) for field in values):
            raise ValueError("At least one field must be provided for update.")
        return values


class UserResponse(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, example=str(uuid.uuid4()))
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED")
    is_professional: Optional[bool] = Field(default=False, example=True)


class LoginRequest(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")


class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="The requested resource was not found.")


class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(
        ..., 
        example=[
            {
                "id": str(uuid.uuid4()),
                "nickname": "john_doe123",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "bio": "Experienced developer",
                "role": "AUTHENTICATED",
                "profile_picture_url": "https://example.com/profiles/john.jpg",
                "linkedin_profile_url": "https://linkedin.com/in/johndoe",
                "github_profile_url": "https://github.com/johndoe",
            }
        ]
    )
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
