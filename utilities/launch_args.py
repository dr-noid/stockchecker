import sys


def parse_args():
    if not len(sys.argv) > 0:
        return

    if "--reset" in sys.argv:
        print("--reset passed as launch arg")


if __name__ == "__main__":
    parse_args()
