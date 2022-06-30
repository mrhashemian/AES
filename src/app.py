from config import config

from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.api_v1_0.routers import router as api_router_v1_0
from fastapi.exceptions import RequestValidationError
import logging
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

app = FastAPI(title=config.app_title)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(api_router_v1_0, prefix='/api_v1.0')


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc: RequestValidationError):
    errors = []
    for e in exc.errors():
        loc = '>'.join([str(item) for item in e['loc'] if item != "body"])
        errors.append({"message": e['msg'], "error_code": 0, "fields": [loc]})
    return JSONResponse(content=errors, status_code=HTTP_400_BAD_REQUEST)


logging.basicConfig(level=config.log_level)
logging.info("application starts...")

if config.debug and __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, debug=False)
