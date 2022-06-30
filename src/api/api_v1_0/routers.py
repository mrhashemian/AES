from fastapi import APIRouter
from starlette.status import HTTP_404_NOT_FOUND
from api.api_v1_0.endpoints.symmetric import router as general_router

router = APIRouter()

router.include_router(general_router, responses={HTTP_404_NOT_FOUND: {"description": "Not found"}},
                      tags=["symmetric"])
