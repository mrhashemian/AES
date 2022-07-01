from fastapi import APIRouter
from starlette.status import HTTP_404_NOT_FOUND
from api.api_v1_0.endpoints.symmetric import router as symmetric_router
from api.api_v1_0.endpoints.hash import router as hash_router

router = APIRouter()

router.include_router(symmetric_router, responses={HTTP_404_NOT_FOUND: {"description": "Not found"}},
                      tags=["symmetric"], prefix='/symmetric')
router.include_router(hash_router, responses={HTTP_404_NOT_FOUND: {"description": "Not found"}},
                      tags=["hash"], prefix='/hash')
