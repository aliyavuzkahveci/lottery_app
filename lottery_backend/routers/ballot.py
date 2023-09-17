"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Implementation of Lottery Ballot related endpoints

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import datetime
import typing

import structlog
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlmodel import Session
from starlette import status

from lottery_backend.database import add_ballot_for_user
from lottery_backend.database import check_ballot_existence
from lottery_backend.database import clear_ballots_on_date
from lottery_backend.database import get_ballots_for_date
from lottery_backend.database import get_session
from lottery_backend.db_models.user import User
from lottery_backend.routers.auth import get_current_user

BALLOT_LENGTH = 16
LOGGER = structlog.get_logger()
router = APIRouter(prefix="/ballot")


@router.post("/submit")
async def submit_ballot(
    ballot: str,
    date: datetime.date,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> typing.Dict[str, str]:
    """
    Enables the user to submit a ballot for a specific date

    Args:

        ballot: a unique 16-digit ballot number to be included in the lottery
        date: a specific day for which the ballot will be added to
        session: a unique session for DB connection
        user: logged in user details

    Returns:

        operation result with some detail message
    """
    _control_input_params_validity(ballot, date)

    if check_ballot_existence(ballot, date, session):
        error_message = f"There is already a ballot:'{ballot}' for the day:'{date}'"
        LOGGER.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=error_message,
        )
    new_user_ballot = add_ballot_for_user(
        user_id=user.id, ballot=ballot, date=date, session=session
    )
    if not new_user_ballot:
        error_message = f"An unknown error occurred while adding the ballot:'{ballot}' for lottery day:'{date}'"
        LOGGER.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )
    return {
        "result": "successful",
        "message": f"Ballot:'{ballot}' is successfully submitted for the lottery day:'{date}'",
    }


@router.get("/list")
async def ballot_list(
    date: datetime.date,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> typing.List[str]:
    """
    Enables the user to list the registered ballots on a certain day

    Args:

        date: a specific day for which the winner ballot is asked
        session: a unique session for DB connection
        user: logged in user details

    Returns:

          list of ballots
    """
    return get_ballots_for_date(date=date, session=session)


# @router.post("/clear")
async def remove_on_date(
    date: datetime.date,
    exception_ballot: typing.Optional[str] = None,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> None:
    """
    Enables the user to list the registered ballots on a certain day

    Args:

        date: a specific day for which the winner ballot is asked
        exception_ballot: 16-digit string representing a ballot for lottery
        session: a unique session for DB connection
        user: logged in user details

    Returns:

          list of ballots
    """
    clear_ballots_on_date(date, exception_ballot, session)


@router.get("/winner")
async def winner_ballot(
    date: datetime.date,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),  # noqa: WPS404
) -> typing.Dict[str, str]:
    """
    Enables the user to get the winner ballot for a specific date

    Args:

        date: a specific day for which the winner ballot is asked
        session: a unique session for DB connection
        user: logged in user details

    Returns:

        operation result with some detail message
    """
    if not _is_date_past(date):
        error_message = (
            f"The lottery for date:'{date}' is still open. So, there is no winner yet!"
        )
        LOGGER.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=error_message,
        )
    winner = _get_winner_ballot(date, session)
    return {
        "result": "successful",
        "message": f"The winner ballot for the day:'{date}' is '{winner}'",
    }


def _get_winner_ballot(date: datetime.date, session: Session) -> str:
    """
    Fetches the ballot list from DB and checks if there is only one ballot which is winner

    Args:
        date: a specific day for which the winner ballot is asked
        session: a unique session for DB connection

    Returns:
        winner ballot as string

    Raises:
         HttpException if there is no winner ballot
    """
    ballots = get_ballots_for_date(date=date, session=session)
    if not ballots:
        error_message = f"No ballot submitted for the given date:'{date}'. So, lottery event didn't take place!"
        LOGGER.warning(error_message)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message,
        )
    elif len(ballots) > 1:
        error_message = f"Lottery event didn't take place for date:'{date}'! An unknown issue has occurred!"
        LOGGER.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )
    return ballots[0]


def _control_input_params_validity(ballot: str, date: datetime.date) -> None:
    """
    Controls the validity of input parameters for submit_ballot endpoint

    Args:
        ballot: a 16-digit string representing a ballot for a lottery
        date: specific day for lottery

    Raises:
        HttpException if input parameter(s) are invalid
    """
    validity_failed = False
    error_messages: typing.List[str] = []
    if not _check_ballot_validity(ballot):
        validity_failed = True
        error_messages.append(
            f"Ballot:'{ballot}' does not conform with the expected format. It should be a 16-digit string!",
        )
    if _is_date_past(date):
        validity_failed = True
        error_messages.append(f"A ballot cannot be submitted for a past date:'{date}'!")

    if validity_failed:
        LOGGER.error(error_messages)
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=error_messages,
        )


def _check_ballot_validity(ballot: str) -> bool:
    """
    Checks if the provided ballot conforms with the criteria

    Args:
        ballot: expected to be a 16-digit string

    Returns:
        True if provided string is a 16-digit number, False otherwise
    """
    if len(ballot) == BALLOT_LENGTH and ballot.isdigit():
        LOGGER.info(f"Ballot:'{ballot}' is valid.")
        return True
    LOGGER.warning(f"Ballot:'{ballot}' is invalid!")
    return False


def _is_date_past(date: datetime.date) -> bool:
    """
    Checks if the provided date is not past

    Args:
         date: day object

    Returns:
        True if the provided date is not past, False otherwise
    """
    current_day = datetime.datetime.now().date()
    if current_day > date:
        LOGGER.info(
            f"The provided date:'{date}' is already past. Today is '{current_day}'",
        )
        return True
    return False
