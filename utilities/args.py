"""This module contains funcionality for launch arguments and env variables"""
import os
import sys

os.environ["DB"] = "False"


def parse_args():
    if len(sys.argv) == 1:
        return

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "db" or "database":
            os.environ["DB"] = "True"
            print("database enabled")
