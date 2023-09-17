"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Entry point for Lottery Backend application.

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import sys

import uvicorn


def main() -> None:
    """
    Main function, prints the version of the library. Can be called from the terminal.
    """
    uvicorn.run("lottery_backend.lottery:app", reload=True, host="0.0.0.0")


if __name__ == "__main__":
    sys.exit(main())
