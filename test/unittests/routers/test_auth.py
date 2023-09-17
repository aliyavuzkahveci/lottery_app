"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Unit tests to test classes/functions in auth.py

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from lottery_backend.database import get_session
from lottery_backend.db_models.user import UserOutput
from test.unittests.conftest import DEFAULT_USER, DEFAULT_NAME, DEFAULT_PASS

from lottery_backend.routers.auth import get_current_user, login


pytest_plugins = ('pytest_asyncio',)


@pytest.mark.parametrize(
    "username, user_object",
    [
        (DEFAULT_USER, UserOutput(id=1, username=DEFAULT_USER, full_name=DEFAULT_NAME)),
        ("NonExistingUser", None,)
    ],
)
def test_get_current_user(username, user_object):
    """
    Tests the logged in user

    Args:
        username: name of the user
        user_object: expected return object
    """
    if user_object:
        user_output = get_current_user(token=username, session=next(get_session()))
        assert user_output.username == user_object.username
        assert user_output.full_name == user_object.full_name
    else:
        with pytest.raises(HTTPException):
            get_current_user(token=username, session=next(get_session()))


@pytest.mark.parametrize(
    "username, password, response",
    [
        (DEFAULT_USER, DEFAULT_PASS, {"access_token": DEFAULT_USER, "token_type": "bearer"}),
        (DEFAULT_USER, "incorrect_pass", None,),
        ("NonExistingUser", DEFAULT_PASS, None,),
    ],
)
@pytest.mark.asyncio
async def test_login(username, password, response):
    """
    Tests the login endpoint

    Args:
        username: name of the user
        password: password of the user
        response: returning response content
    """
    if response:
        response_dict = await login(
            form_data=OAuth2PasswordRequestForm(username=username, password=password),
            session=next(get_session()),
        )
        assert response_dict["access_token"] == response["access_token"]
        assert response_dict["token_type"] == response["token_type"]
    else:
        with pytest.raises(HTTPException):
            await login(
                form_data=OAuth2PasswordRequestForm(username=username, password=password),
                session=next(get_session()),
            )
