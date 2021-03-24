from typing import Optional

from pydantic import EmailStr, HttpUrl
from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel


# The 5 model types we just defined demonstrate a pattern
# that will be used for almost every resource:
#
# - Base   - all shared attributes of a resource
# - Create - attributes required to create a new resource - used at POST requests
# - Update - attributes that can be updated - used at PUT requests
# - InDB   - attributes present on any resource coming out of the database
# - Public - attributes present on public facing
#            resources being returned from GET, POST, and PUT requests


class ProfileBase(CoreModel):
    full_name: Optional[str]
    phone_number: Optional[str]
    bio: Optional[str]
    image: Optional[HttpUrl]


class ProfileCreate(ProfileBase):
    """
    The only field required to create a profile is the users id
    """

    user_id: int


class ProfileUpdate(ProfileBase):
    """
    Allow users to update any or no fields, as long as it's not user_id
    """

    pass


class ProfileInDB(IDModelMixin, DateTimeModelMixin, ProfileBase):
    user_id: int
    username: Optional[str]
    email: Optional[EmailStr]


class ProfilePublic(ProfileInDB):
    pass