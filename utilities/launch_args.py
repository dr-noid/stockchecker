import sys

from utilities.settings import program_settings


def parse_args() -> None:
    if not len(sys.argv) > 0:
        return None

    args = sys.argv[1:]

    for arg in args:
        if arg in ("--keep", "-K"):
            program_settings.db_reset = False

    for arg in args:
        if arg in ("--notif", "--notifications", "-N"):
            program_settings.notifications = True


if __name__ == "__main__":
    pass
