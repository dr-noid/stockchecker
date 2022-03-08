from enum import Enum

from persistence.database import Base


class GPU(Enum):
    RTX3060 = 0
    RTX3060TI = 1
    RTX3070 = 2
    RTX3070TI = 3
    RTX3080 = 4
    RTX3080TI = 5
    RTX3090 = 6


if __name__ == '__main__':
    pass
