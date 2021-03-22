from typing import Optional

from pydantic import EmailStr, constr

from app.models.core import CoreModel, DateTimeModelMixin, IDModelMixin


class UserBase(CoreModel):
    """
    Leaving off password and salt from base model
    """

    email: Optional[EmailStr]
    username: Optional[str]
    email_verfieid: bool = False
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(CoreModel):
    """
    Email, username, and password are required for registering a new user
    """

    email: EmailStr
    password: constr(min_length=8, max_length=100)

    # We're ensuring that all passwords have a minimum length
    # of 7 and a maximum length of 100. Not sure anyone would
    # ever have a password with 100 characters, but it's
    # nice to show off that feature.
    username: constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")


class UserUpdate(CoreModel):
    """
    Users are allowed to update their email and username
    """

    email: Optional[EmailStr]
    username: Optional[constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")]


class UserPasswordUpdate(CoreModel):
    """
    Users can change their password
    """

    password: constr(min_length=7, max_length=100)
    salt: str


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """

    password: constr(min_length=7, max_length=100)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    pass
