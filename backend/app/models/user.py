from typing import Optional

from pydantic import EmailStr, constr

from app.models.core import CoreModel, DateTimeModelMixin, IDModelMixin
from app.models.token import AccessToken

from app.models.profile import ProfilePublic

# The 5 model types we just defined demonstrate a pattern
# that will be used for almost every resource:
#
# - Base   - all shared attributes of a resource
# - Create - attributes required to create a new resource - used at POST requests
# - Update - attributes that can be updated - used at PUT requests
# - InDB   - attributes present on any resource coming out of the database
# - Public - attributes present on public facing
#            resources being returned from GET, POST, and PUT requests


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

    # salt here is a bit useless, since the library used to generate the
    # hashed password make use of an internal salt on its own.
    # salt here will be empty.
    salt: str


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """

    password: constr(min_length=7, max_length=100)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    access_token: Optional[AccessToken]
    profile: Optional[ProfilePublic]
