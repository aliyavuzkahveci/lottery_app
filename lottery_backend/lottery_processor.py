"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Implementation of Lottery Processor class having a scheduled task to draw lottery everyday

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import datetime
import random
import threading
import time

import schedule
import structlog

from lottery_backend.database import clear_ballots_on_date
from lottery_backend.database import get_ballots_for_date
from lottery_backend.exceptions import catch_exceptions

LOGGER = structlog.get_logger()
THREAD_SLEEP_TIME = 1  # seconds


class LotteryProcessor(threading.Thread):
    """Thread-based class to executed a scheduled task in the background."""

    def __init__(self) -> None:
        """
        Initializes the LotteryProcessor object
        """
        super().__init__()
        self.stop_requested = False
        schedule.every(1).day.at("00:00").do(self._draw_lottery)

    def stop(self) -> None:
        """Sets the member variable flag to stop execution"""
        self.stop_requested = True
        LOGGER.info("Lottery Processor is asked to stop its execution!")

    def run(self) -> None:
        """
        Periodically executes the pending scheduled tasks
        """
        LOGGER.info(
            "Starting thread to periodically run the pending scheduled tasks in the background."
        )
        while not self.stop_requested:
            schedule.run_pending()
            time.sleep(THREAD_SLEEP_TIME)

        LOGGER.info(
            "Thread existed from the while loop! Cancelling te scheduled task..."
        )
        schedule.clear()  # cancels/removes any scheduled task

    @classmethod
    @catch_exceptions()
    def _draw_lottery(cls) -> None:
        """
        Performs lottery draw for the completed day since lottery is drawn at midnight
        """
        previous_day = datetime.datetime.now().date() - datetime.timedelta(days=1)
        ballots = get_ballots_for_date(date=previous_day)
        if not ballots:
            LOGGER.warning(
                "For a lottery to be drawn, at least one ballot should exist!"
            )
            return
        winning_ballot = random.choice(ballots)
        LOGGER.info(f"Winning ballot for the day:'{previous_day}' is {winning_ballot}")
        clear_ballots_on_date(date=previous_day, exception_ballot=winning_ballot)
        LOGGER.info("Lottery draw is completed successfully...")
