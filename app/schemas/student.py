from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    EmailStr
)


class StudentCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    age: int = Field(
        gt=0,
        le=100
    )

    course: str = Field(
        min_length=2,
        max_length=100
    )


class StudentUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    email: EmailStr | None = None

    age: int | None = Field(
        default=None,
        gt=0,
        le=100
    )

    course: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )


class StudentResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    age: int
    course: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
class CICDTestRequest(BaseModel):
    message: str
    version: str
