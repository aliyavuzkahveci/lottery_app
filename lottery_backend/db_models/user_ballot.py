"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Implementation of Database Model class to keep Users' ballots

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import datetime
import typing

from sqlmodel import Field
from sqlmodel import SQLModel


class UserBallot(SQLModel, table=True):
    """Represents users having ballots"""

    id: typing.Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False)  # primary key of the User Table
    ballot: str = Field(nullable=False)  # will be checked to conform if 16-digit number!
    date: datetime.date = Field(default_factory=datetime.date.today, nullable=False)
