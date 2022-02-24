import sys

settings_dict = {"db_reset": False}


def parse_args() -> dict[str, bool]:
    if not len(sys.argv) > 0:
        return settings_dict

    if ("--reset", "-R") in sys.argv:
        settings_dict["db_reset"] = True

    return settings_dict


if __name__ == "__main__":
    pass
