"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Enablers to test the code

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import pytest
from sqlmodel import SQLModel, Session, select

from lottery_backend.database import engine
from lottery_backend.db_models.user import User

DEFAULT_USER = "ayk"
DEFAULT_PASS = "12345"
DEFAULT_NAME = "Ali Yavuz Kahveci"
DEFAULT_BALLOT = "1234567891234567"


@pytest.fixture(autouse=True)
def initialize_db():
    """
    Adds a default user to the DB
    """
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        query = select(User).where(User.username == DEFAULT_USER)
        user = session.exec(query).first()
        if user:  # user already exists
            return
        user = User(
            username=DEFAULT_USER,
            full_name=DEFAULT_NAME,
            email_address="ayk_sample@email.com",
            phone_number="0612345678",
        )
        user.set_password(DEFAULT_PASS)
        session.add(user)
        session.commit()


def remove_user(username: str):
    """
    Removes the user from the DB

    Args:
        username: name of the user
    """
    with Session(engine) as session:
        query = select(User).where(User.username == username)
        user = session.exec(query).first()
        if not user:
            return
        session.delete(user)
        session.commit()
