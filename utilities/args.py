"""This module contains funcionality for launch arguments and env variables"""
import sys


def parse_args():
    if len(sys.argv) == 1:
        return

    # for i in range(1, len(sys.argv)):
    #     if sys.argv[i] == "db" or "database":
    #         os.environ["DB"] = "1"
    #         print("database enabled")
