"""This module contains funcionality for launch arguments and env variables"""
import sys


def parse_args():
    if len(sys.argv) == 1:
        return
