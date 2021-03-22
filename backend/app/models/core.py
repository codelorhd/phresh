from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here.
    """

    pass


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # the validator decorator - to set a default datetime
    # for both the created_at and updated_at fields
    # https://pydantic-docs.helpmanual.io/usage/validators/
    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now()


class IDModelMixin(BaseModel):
    id: int
