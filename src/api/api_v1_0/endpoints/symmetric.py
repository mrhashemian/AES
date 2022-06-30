from typing_extensions import Literal
from fastapi import APIRouter
from api.schemas.symmetric.aes_schema import AESSchema, TDESSchema
from services.symmetric.aes_service import AESService
from services.symmetric.triple_des_service import TripleDESService

router = APIRouter()


@router.post("/aes/{mode}")
def aes_algorithm(mode: Literal["encrypt", "decrypt"], data: AESSchema):
    return AESService(key=data.key, mode=mode, text=data.text).execute()


@router.post("/3des/{mode}")
def triple_des_algorithm(mode: Literal["encrypt", "decrypt"], data: TDESSchema):
    return TripleDESService(key=data.key, mode=mode, text=data.text).execute()
