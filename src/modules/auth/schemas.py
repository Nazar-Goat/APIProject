from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )
    username: str = Field(
        min_length=1,
        max_length=50,
    )


class UserRegisterOutSchema(BaseModel):
    id: PydanticObjectId
    email: EmailStr
    username: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class CurrentUserSchema(BaseModel):
    id: PydanticObjectId
    email: EmailStr
    username: str