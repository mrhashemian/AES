from api.schemas.base_schema import BaseSchema


class HashSchema(BaseSchema):
    text: str


class HMACSchema(BaseSchema):
    secret: str
    plain_text: str


class HMACVerifySchema(HMACSchema):
    hashed_text: str
