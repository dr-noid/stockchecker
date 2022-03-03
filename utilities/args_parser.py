import sys

from dotenv import dotenv_values, load_dotenv

x = dotenv_values("config/.env")
print(load_dotenv("config/.env"))

print(x)

settings_dict = {"db_reset": True,
                 "notifs": False}


def parse_args() -> dict[str, bool]:
    if not len(sys.argv) > 0:
        return settings_dict

    args = sys.argv[1:]

    for arg in args:
        if arg in ("--keep", "-K"):
            settings_dict["db_reset"] = False

    for arg in args:
        if arg in ("--notifications", "--notifs", "-N"):
            settings_dict["notifs"] = True

    return settings_dict


if __name__ == "__main__":
    pass
