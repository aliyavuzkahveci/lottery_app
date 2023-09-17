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
import datetime

import pytest
from fastapi import HTTPException

from lottery_backend.database import fetch_user_from_db, add_ballot_for_user, get_session, clear_ballots_on_date
from lottery_backend.routers.ballot import _check_ballot_validity, _is_date_past, _control_input_params_validity, \
    _get_winner_ballot, winner_ballot, ballot_list, submit_ballot
from test.unittests.conftest import DEFAULT_BALLOT, DEFAULT_USER

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.parametrize(
    "ballot, date, exception_raised",
    [
        (DEFAULT_BALLOT, datetime.date.today() + datetime.timedelta(days=1), {}),  # valid ballot & date
        (DEFAULT_BALLOT, datetime.date.today() + datetime.timedelta(days=1), False),  # existing ballot
        ("123456789", datetime.date.today(), True),  # invalid ballot
        ("1234567890987654", datetime.date.today() - datetime.timedelta(days=1), True),  # invalid date
    ],
)
@pytest.mark.asyncio
async def test_submit_ballot(ballot, date, exception_raised):
    """
    Tests the endpoint submit_ballot

    Args:
        ballot: string to represent ballot in a lottery
        date: datetime object representing the day
        exception_raised: flag to check if exception is expected
    """
    clear_ballots_on_date(date)  # clear the DB in case a previous run is interrupted!
    user = fetch_user_from_db(DEFAULT_USER)
    assert user  # make sure there is user
    if exception_raised:
        with pytest.raises(HTTPException):
            await submit_ballot(ballot, date, next(get_session()), user)
    else:
        response = await submit_ballot(ballot, date, next(get_session()), user)
        assert response["result"] == "successful"
    clear_ballots_on_date(date)  # clear the DB


@pytest.mark.parametrize(
    "date, expected_ballot_count",
    [
        (datetime.date.today() - datetime.timedelta(days=1), 1),
        (datetime.date.today() - datetime.timedelta(days=2), 0),
        (datetime.date.today() - datetime.timedelta(days=3), 3),
    ],
)
@pytest.mark.asyncio
async def test_ballot_list(date, expected_ballot_count):
    """
    Tests the endpoint ballot_list

    Args:
        date: datetime object representing the day
        expected_ballot_count: ballot count in the returning list
    """
    clear_ballots_on_date(date)  # clear the DB in case a previous run is interrupted!
    prepare_ballots_on_date(date)
    ballots = await ballot_list(date, next(get_session()))
    assert len(ballots) == expected_ballot_count
    clear_ballots_on_date(date)  # clear the DB


@pytest.mark.parametrize(
    "date, winner",
    [
        (datetime.date.today(), None),  # lottery is open for the day
        (datetime.date.today() - datetime.timedelta(days=1), DEFAULT_BALLOT),  # winner ballot will be received
    ],
)
@pytest.mark.asyncio
async def test_winner_ballot(date, winner):
    """
    Tests the endpoint winner_ballot

    Args:
        date: datetime object representing the day
        winner: winner ballot for the given day
    """
    if winner:  # expecting a happy path
        clear_ballots_on_date(date)  # clear the DB in case a previous run is interrupted!
        prepare_ballots_on_date(date)
        response = await winner_ballot(date, next(get_session()))
        assert response["result"] == "successful"
        clear_ballots_on_date(date)  # clear the DB
    else:
        with pytest.raises(HTTPException):
            await winner_ballot(date, next(get_session()))



@pytest.mark.parametrize(
    "date, expected_ballot",
    [
        (datetime.date.today() - datetime.timedelta(days=1), DEFAULT_BALLOT),  # one ballot on date
        (datetime.date.today() - datetime.timedelta(days=2), None),  # no ballot on date
        (datetime.date.today() - datetime.timedelta(days=3), None),  # multiple ballots on date
    ],
)
def test_get_winner_ballot(date, expected_ballot):
    """
    Tests getting the winner ballot

    Args:
         date: datetime object of a day
         expected_ballot: expected ballot as the winner
    """
    clear_ballots_on_date(date)  # clear the DB in case a previous run is interrupted!
    prepare_ballots_on_date(date)
    if expected_ballot:
        assert _get_winner_ballot(date, next(get_session())) == expected_ballot
    else:
        with pytest.raises(HTTPException):
            _get_winner_ballot(date, next(get_session()))
            assert False  # make sure code does not reach here!
    clear_ballots_on_date(date)  # clear the DB


@pytest.mark.parametrize(
    "ballot, date, exception_raised",
    [
        (DEFAULT_BALLOT, datetime.date.today() + datetime.timedelta(days=1), False),  # valid balot & date
        ("123456789", datetime.date.today(), True),  # invalid ballot
        (DEFAULT_BALLOT, datetime.date.today() - datetime.timedelta(days=1), True),  # invalid date
    ],
)
def test_control_input_params_validity(ballot, date, exception_raised):
    """
    Tests the validity of input parameters ballot and date

    Args:
        ballot: string to represent ballot in a lottery
        date: datetime object representing the day
        exception_raised: Flag to indicate an exception will be raised
    """
    if exception_raised:
        with pytest.raises(HTTPException):
            _control_input_params_validity(ballot, date)
    else:
        _control_input_params_validity(ballot, date)
        assert True  # means code reaches here without any exception


@pytest.mark.parametrize(
    "ballot, expected_return",
    [
        (DEFAULT_BALLOT, True),  # valid ballot
        ("123456789", False),  # invalid ballot: length should be 16
        ("123456789AB34567", False),  # invalid ballot: should contain only digits
    ],
)
def test_check_ballot_validity(ballot, expected_return):
    """
    Tests the validity of a ballot

    Args:
        ballot: string to represent ballot in a lottery
        expected_return: expected return value of a function call _check_ballot_validity
    """
    assert _check_ballot_validity(ballot) == expected_return


@pytest.mark.parametrize(
    "date, expected_return",
    [
        (datetime.date.today(), False),  # today
        (datetime.date.today() + datetime.timedelta(days=1), False),  # tomorrow
        (datetime.date.today() - datetime.timedelta(days=1), True),  # yesterday
    ],
)
def test_is_date_past(date, expected_return):
    """
    Tests the date object if it is the past day

    Args:
        date: datetime object representing the day
        expected_return: expected return value of a function call _is_date_past
    """
    assert _is_date_past(date) == expected_return


def prepare_ballots_on_date(date):
    """
    Prepares the DB by inserting ballots

    Args:
         date: datetime object representing the day
    """
    user = fetch_user_from_db(DEFAULT_USER)
    assert user  # make sure there is user
    diff = datetime.date.today() - date
    if diff == datetime.timedelta(days=1):
        add_ballot_for_user(user.id, DEFAULT_BALLOT, date)
    elif diff == datetime.timedelta(days=3):
        add_ballot_for_user(user.id, DEFAULT_BALLOT, date)
        add_ballot_for_user(user.id, "9876543211234567", date)
        add_ballot_for_user(user.id, "9876543217654321", date)
