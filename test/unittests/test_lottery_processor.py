"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Unit tests to test classes/functions in lottery_processor.py

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
from time import sleep

import schedule

from lottery_backend import lottery_processor
from lottery_backend.lottery_processor import LotteryProcessor
from test.unittests.conftest import DEFAULT_BALLOT


def test_lottery_processor(monkeypatch):
    """
    Tests the lottery processor class functionality and internal structures

    Args:
        monkeypatch: To stub some functions
    """
    def stub_get_ballots_for_date(*_args, **_kwargs):
        """Returns mocked ballot list"""
        return [DEFAULT_BALLOT, "9876543211234567", "1928374654637281"]

    def stub_clear_ballots_on_date(*_args, **_kwargs):
        """Stubs the DB operation"""
        pass

    monkeypatch.setattr(lottery_processor, "get_ballots_for_date", stub_get_ballots_for_date)
    monkeypatch.setattr(lottery_processor, "clear_ballots_on_date", stub_clear_ballots_on_date)

    assert not schedule.get_jobs()  # there is no scheduled job
    lottery_proc = lottery_processor.LotteryProcessor()
    assert len(schedule.get_jobs()) == 1  # LotteryProcessor introduced a scheduled task
    lottery_proc.start()
    sleep(5)  # wait for a couple of thread iterations
    assert not lottery_proc.stop_requested
    lottery_proc.stop()
    assert lottery_proc.stop_requested
    lottery_proc.join()
    assert not schedule.get_jobs()  # the scheduled job is cancelled
