"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Implementation of User related endpoints

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import typing

import structlog
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlmodel import Session
from starlette import status

from lottery_backend.database import add_new_user
from lottery_backend.database import fetch_user_from_db
from lottery_backend.database import get_session
from lottery_backend.db_models.user import UserOutput

LOGGER = structlog.get_logger()
router = APIRouter(prefix="/user")


@router.post("/register", response_model=UserOutput)
async def register(  # noqa: WPS211
    username: str,
    password: str,
    full_name: str,
    email_address: typing.Optional[str] = None,
    phone_number: typing.Optional[str] = None,
    session: Session = Depends(get_session),
) -> UserOutput:
    """
    Adds a new user to the database.

    Args:

        username: name of the new user
        password: password of the new user
        full_name: new user's name and surname
        email_address: an optional communication detail for a user
        phone_number: an optional communication detail for a user
        session: a unique session for DB connection

    Returns:

        a newly created user object
    """
    user = fetch_user_from_db(username=username, session=session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"There is already a user registered with username:'{username}'",
        )
    new_user = add_new_user(
        username,
        password,
        full_name,
        email_address,
        phone_number,
        session,
    )
    return UserOutput.from_orm(new_user)
