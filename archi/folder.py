import pathlib

from .struct import Struct
from .state import State
from .action import Action
from utils import choice_message

class Folder(Struct):

  contains_comparator : dict = {
    str: lambda x, y: x.name == y,
  }

  def __init__(self, name : str, children : list = None):
    super().__init__(name)
    self.children : list = children if children else []

  def __str__(self, prefix : str = '', last_prefix : str = '', **kwargs) -> str:
    child_before = prefix + ( '│ ' if last_prefix == '├─' else '  ')

    lenght = len(self.children)
    s = prefix + last_prefix + '📁' + super().__str__(**kwargs)
    if kwargs.get('reclusive', True):
      for i in range(lenght - 1):
        s += '\n' + self.children[i].__str__(child_before, '├─')
      if lenght:
        s += '\n' + self.children[lenght - 1].__str__(child_before, '└─')
    return s

  def type_check(self, path : pathlib.Path) -> bool:
    return path.is_dir()

  def create_element(self, path : str = '', **kwargs):
    path.mkdir(parents=True, exist_ok=True)

  def create_children(self, parrent : str = '', action : Action = Action.COMPLET, prefix : str = '', last_prefix : str = '', **kwargs):
    child_before = prefix + ( '│ ' if last_prefix == '├─' else '  ')
    lenght = len(self.children)
    for i in range(lenght - 1):
      self.children[i].create(parrent + self.name + '/', action, child_before,  '├─', **kwargs)
    if lenght:
      self.children[lenght - 1].create(parrent + self.name + '/', action, child_before,  '└─', **kwargs)

  def contains(self, x : str) -> bool:
    return self.__contains__(x, True)

  def __contains__(self, x : str, reclursive = False) -> bool:
    comparator = Folder.contains_comparator.get(type(x), lambda x, y: x == y)

    for child in self.children:
      if comparator(child, x):
        return True
      if reclursive and isinstance(child, Folder) and child.__contains__(x, reclursive):
        return True

    return False
