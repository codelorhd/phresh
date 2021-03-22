from typing import Optional
from enum import Enum

from app.models.core import CoreModel, IDModelMixin


# The 5 model types we just defined demonstrate a pattern
# that will be used for almost every resource:
#
# - Base   - all shared attributes of a resource
# - Create - attributes required to create a new resource - used at POST requests
# - Update - attributes that can be updated - used at PUT requests
# - InDB   - attributes present on any resource coming out of the database
# - Public - attributes present on public facing
#            resources being returned from GET, POST, and PUT requests


# We want to restrict the number of valid inputs to an explicit set,
class CleaningType(str, Enum):
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"


class CleaningBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """

    # We use the Optional type declaration to specify that
    # any attribute not passed in when creating the model
    # instance will be set to None.

    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    cleaning_type: Optional[CleaningType] = "spot_clean"


class CleaningCreate(CleaningBase):
    name: str
    price: float


class CleaningUpdate(CleaningBase):
    cleaning_type: Optional[CleaningType]


class CleaningInDB(IDModelMixin, CleaningBase):
    name: str
    price: float
    cleaning_type: CleaningType


class CleaningPublic(IDModelMixin, CleaningBase):
    pass
