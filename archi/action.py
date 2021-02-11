from enum import Enum, unique

@unique
class Action(bytes, Enum):

  def __new__(cls, value : int, icon : str = '', color : int = 0):
    obj = bytes.__new__(cls, [value])
    obj._value_ = value
    obj.icon = icon
    obj.color = f'\033[{color}m'
    return obj

  SKIP= (0, '→', 90 )
  COMPLET = (1, '✔', 32)
  ABOARDED = (2, '✘', 31)