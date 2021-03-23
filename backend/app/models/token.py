from datetime import datetime, timedelta

from pydantic import EmailStr

from app.core.config import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.core import CoreModel


class JWTMeta(CoreModel):
    iss: str = "phresh.io"  # issuer of the token (us #winks)
    aud: str = JWT_AUDIENCE  # who this token is intended for
    iat: float = datetime.timestamp(datetime.utcnow())  # when this token was issued at
    exp: float = datetime.timestamp(
        datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )  # when this token expires and is no longer valid proof that ther requesting user is logged in


class JWTCreds(CoreModel):
    """ How we'll identify users"""

    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - comibne meta and username
    """

    pass


class AccessToken(CoreModel):
    access_token: str
    token_type: str