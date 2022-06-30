from typing import Optional

from api.schemas.base_schema import BaseSchema


class AESSchema(BaseSchema):
    key: str
    text: str


class TDESSchema(BaseSchema):
    key: Optional[str] = None
    text: str
