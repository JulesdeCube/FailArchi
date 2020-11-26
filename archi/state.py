from enum import Enum, unique

@unique
class State(bytes, Enum):

  def __new__(cls, value : int, icon : str = '', color : int = 0):
    obj = bytes.__new__(cls, [value])
    obj._value_ = value
    obj.icon = icon
    obj.color = f'\033[{color}m'
    return obj

  WONG_TYPE = (0, '⚠', 33)
  NOT_EXIST = (1, '✘', 31)
  UNKOWN = (2, )
  EXIST = (3, '✔', 32)