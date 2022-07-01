from typing_extensions import Literal
from fastapi import APIRouter
from api.schemas.symmetric.aes_schema import AESSchema, TDESSchema
from config.enums import AESMode, TDESMode
from services.symmetric.aes_service import AESService
from services.symmetric.triple_des_service import TripleDESService

router = APIRouter()


@router.post("/aes/{action}")
def aes_algorithm(action: Literal["encrypt", "decrypt"], mode: Literal[tuple(AESMode.get_value_dict().values())],
                  data: AESSchema):
    return AESService(key=data.key, action=action, text=data.text, mode=mode).execute()


@router.post("/3des/{action}")
def triple_des_algorithm(action: Literal["encrypt", "decrypt"],
                         mode: Literal[tuple(TDESMode.get_value_dict().values())],
                         data: TDESSchema):
    return TripleDESService(key=data.key, action=action, text=data.text, mode=mode).execute()
