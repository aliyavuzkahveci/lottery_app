"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Implementation of Database related functionalities

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import datetime
import typing
from pathlib import Path

import structlog
from sqlmodel import Session
from sqlmodel import create_engine
from sqlmodel import select

from lottery_backend.db_models.user import User
from lottery_backend.db_models.user_ballot import UserBallot

LOGGER = structlog.get_logger()
DB_PATH = Path(__file__).parents[0] / "lottery.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True,  # Log generated SQL
)


def get_session():
    with Session(engine) as session:
        yield session


def add_new_user(  # noqa: WPS211
    username: str,
    password: str,
    full_name: str,
    email_address: typing.Optional[str] = None,
    phone_number: typing.Optional[str] = None,
    session: Session = next(get_session()),
) -> User:
    """
    Adds a new user into the database

    Args:
        username: a unique username
        password: to be used when logging in
        full_name: name and surname of the user
        email_address: optional communication detail
        phone_number: optional communication detail
        session: session for DB connection

    Returns:
         a newly created User object
    """
    new_user = User(
        username=username,
        full_name=full_name,
        email_address=email_address,
        phone_number=phone_number,
    )
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def fetch_user_from_db(username: str, session: Session = next(get_session())) -> typing.Optional[User]:
    """
    Fetches the User object from the database

    Args:
        username: used as an identifier for User object
        session: session for DB connection

    Returns:
        User object if it exists, None otherwise
    """
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    if user:
        LOGGER.info(f"There exists a user object in DB with the username '{username}'")
    else:
        LOGGER.info(f"There is no user object in DB with the username '{username}'")
    return user


def add_ballot_for_user(
        user_id: int,
        ballot: str,
        date: datetime.date,
        session: Session = next(get_session()),
) -> UserBallot:
    """
    Adds a new ballot on the user for a specific day of lottery

    Args:
        user_id: a unique id of a username in User table
        ballot: a 16-digit string
        date: day of the lottery for which the ballot is added
        session: session for DB connection

    Returns:
         a newly created UserBallot object
    """
    new_user_ballot = UserBallot(user_id=user_id, ballot=ballot, date=date)
    session.add(new_user_ballot)
    session.commit()
    session.refresh(new_user_ballot)
    return new_user_ballot


def get_ballots_for_date(date: datetime.date, session: Session = next(get_session())) -> typing.List[str]:
    """
    Fetches all the submitted ballots for the provided lottery day

    Args:
         date: a day to query the ballots
         session: session for DB connection

    Returns:
        list of ballots in this provided lottery day
    """
    ballot_list: typing.List[str] = []
    query = select(UserBallot).where(UserBallot.date == date)
    user_ballot_list = session.exec(query).all()
    for user_ballot in user_ballot_list:
        ballot_list.append(user_ballot.ballot)
    return ballot_list


def clear_ballots_on_date(
    date: datetime.date,
    exception_ballot: typing.Optional[str] = None,
    session: Session = next(get_session()),
) -> None:
    """
    Deletes the ballots on a given day. If an exception ballot is provided, it won't be removed!

    Args:
        date: a day to query the ballots
        exception_ballot: 16-digit string representing a ballot for lottery
        session: session for DB connection
    """
    if exception_ballot:
        query = select(UserBallot).where(UserBallot.date == date, UserBallot.ballot != exception_ballot)
        LOGGER.info(f"Ballot '{exception_ballot}' will not be removed!")
    else:
        query = select(UserBallot).where(UserBallot.date == date)
    user_ballot_list = session.exec(query).all()
    for user_ballot in user_ballot_list:
        session.delete(user_ballot)
    session.commit()
    LOGGER.info(f"{len(user_ballot_list)} ballots on {date} are deleted from DB!")


def check_ballot_existence(ballot: str, date: datetime.date, session: Session = next(get_session())) -> bool:
    """
    Checks if the ballot exists for the given lottery day

    Args:
        ballot: 16-digit string representing a ballot for lottery
        date: a day to query the ballots
        session: session for DB connection

    Returns:
        list of ballots in this provided lottery day
    """
    query = select(UserBallot).where(UserBallot.ballot == ballot, UserBallot.date == date)
    user_ballot = session.exec(query).first()
    if user_ballot:
        LOGGER.info(f"Ballot:'{ballot}' exists for the day:'{date}'")
        return True
    LOGGER.info(f"Ballot:'{ballot}' does not exist for the day:'{date}'")
    return False
