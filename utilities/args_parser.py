import sys
from os import environ

from dotenv import dotenv_values, load_dotenv

load_dotenv("config/.env")

environ["db_reset"] = "True"
environ["notifs"] = "False"


def parse_args() -> None:
    if not len(sys.argv) > 0:
        return

    args = sys.argv[1:]

    for arg in args:
        if arg in ("--keep", "-K"):
            environ["db_reset"] = "False"

    for arg in args:
        if arg in ("--notifications", "--notifs", "-N"):
            environ["notifs"] = "True"


if __name__ == "__main__":
    pass
