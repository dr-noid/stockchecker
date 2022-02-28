import sys

settings_dict = {"db_reset": True}


def parse_args() -> dict[str, bool]:
    if not len(sys.argv) > 0:
        return settings_dict

    args = sys.argv[1:]

    for arg in args:
        if arg in ("--keep", "-K"):
            settings_dict["db_reset"] = False

    return settings_dict


if __name__ == "__main__":
    pass
