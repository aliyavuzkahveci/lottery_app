"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Implementation of Lottery Backend application initialization

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import structlog
from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from lottery_backend.database import engine
from lottery_backend.exceptions import BadRequestException
from lottery_backend.lottery_processor import LotteryProcessor
from lottery_backend.routers import auth
from lottery_backend.routers import ballot
from lottery_backend.routers import user

LOGGER = structlog.get_logger()
app = FastAPI(title="Lottery Service")
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(ballot.router)
lottery_processor = LotteryProcessor()


origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Executed when application is starting."""
    LOGGER.info("Lottery Backend Service is starting up...")
    SQLModel.metadata.create_all(engine)
    lottery_processor.start()


@app.on_event("shutdown")
def on_shutdown() -> None:
    """Executed when application is shutting down."""
    LOGGER.info("Lottery Backend Service is shutting down...")
    lottery_processor.stop()
    lottery_processor.join()  # wait for threads to finish their execution!


@app.exception_handler(BadRequestException)
async def unicorn_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Bad Request"},
    )
