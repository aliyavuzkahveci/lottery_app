"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Unit tests to test classes/functions in user.py

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import pytest
from fastapi import HTTPException

from lottery_backend.database import get_session
from lottery_backend.db_models.user import UserOutput
from lottery_backend.routers.user import register
from test.unittests.conftest import DEFAULT_USER, DEFAULT_NAME, remove_user

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.parametrize(
    "username, user_object",
    [
        ("ANewUser", UserOutput(id=1, username="ANewUser", full_name=DEFAULT_NAME)),
        (DEFAULT_USER, None),
    ],
)
@pytest.mark.asyncio
async def test_register(username, user_object):
    """
    Tests registering users into db

    Args:
        username: name of the user
        user_object: expected return object
    """
    if user_object:
        remove_user(username)  # in case revious execution is interrupted before deleting the user
        created_user = await register(username, "password", DEFAULT_NAME, "email@email", "123456", next(get_session()))
        assert created_user.username == user_object.username
        assert created_user.full_name == user_object.full_name
        remove_user(username)
    else:
        with pytest.raises(HTTPException):
            await register(username, "password", DEFAULT_NAME, "email@email", "123456", next(get_session()))
