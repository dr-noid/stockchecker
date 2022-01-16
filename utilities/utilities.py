"""This module provides useful utility functions"""


def str_list_from_list(l: list, lower: bool = True) -> list[str]:
    """Returns a list with the objects class name"""
    working_list: list[object] = l.copy()
    if lower:
        return [item.__class__.__name__.lower() for item in working_list]
    return [item.__class__.__name__ for item in working_list]


if __name__ == "__main__":
    pass
