from enum import Enum, unique

@unique
class Action(Enum):

  ABOARDED = 0
  COMPLET = 1
  SKIP = 2
