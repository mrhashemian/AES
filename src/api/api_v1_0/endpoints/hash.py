from fastapi import APIRouter
from typing_extensions import Literal

from api.schemas.hash_schema import HashSchema, HMACSchema, HMACVerifySchema
from services.hash.HMAC_service import HMACService
from services.hash.sha1_service import SHA1Service
from services.hash.sha2_service import SHA2Service
from services.hash.sha3_service import SHA3Service

router = APIRouter()


@router.post("/sha1")
def sha1_algorithm(data: HashSchema):
    return SHA1Service(text=data.text).execute()


@router.post("/sha2")
def sha2_algorithm(data: HashSchema):
    return SHA2Service(text=data.text).execute()


@router.post("/sha3")
def sha3_algorithm(data: HashSchema):
    return SHA3Service(text=data.text).execute()


@router.post("/sha3/encode/{digestmod}")
def hmac_algorithm_encode(digestmod: Literal["SHA1", "SHA256", "SHA512", "SHA3_256", "SHA3_512"],
                          data: HMACSchema):
    return HMACService("encode", data.secret, digestmod, data.plain_text, None).execute()


@router.post("/sha3/verify/{digestmod}")
def hmac_algorithm_verify(digestmod: Literal["SHA1", "SHA256", "SHA512", "SHA3_256", "SHA3_512"],
                          data: HMACVerifySchema):
    return HMACService("verify", data.secret, digestmod, data.plain_text, data.hashed_text).execute()
