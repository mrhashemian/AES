from fastapi import APIRouter
from api.schemas.hash_schema import HashSchema
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
