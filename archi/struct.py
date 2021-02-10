from bs4 import BeautifulSoup
import pathlib

from .state import State
from .action import Action
from utils import choice_message

class Struct(object):

  def __init__(self, name : str):
    self.name : str = self.normalize_name(name)
    self.status : State = State.UNKOWN

  def update(self, path : str = '') -> pathlib.Path:
    path : pathlib.Path = pathlib.Path(path + self.name)
    if path.exists():
        self.status = State.EXIST if self.type_check(path) else State.WONG_TYPE
    else:
      self.status = State.NOT_EXIST
    return path

  def type_check(self, path : pathlib.Path) -> bool:
    raise NotImplementedError()

  def create(self, parrent : str = '', parrent_action : Action = Action.COMPLET, prefix : str = '', last_prefix : str = '', **kwargs):
    path : pathlib.Path = self.update(parrent)
    action : Action = None
    child_before = prefix + ( '│ ' if last_prefix == '├─' else '  ')
    print(self.__str__(prefix, last_prefix, reclusive=False), end='')
    if parrent_action == Action.ABOARDED:
      action = Action.ABOARDED
    elif self.status == State.EXIST:
      action = Action.SKIP
    elif self.status == State.NOT_EXIST:
      self.create_element(path, **kwargs)
      action = Action.COMPLET
    elif self.status == State.WONG_TYPE:
      if choice_message(" wong type, replace it ?"):
        self.remove(path)
        self.create_element(path, **kwargs)
        action = Action.COMPLET
      else:
        action = Action.ABOARDED
    elif self.status == State.UNKOWN:
      raise ValueError('unexprected struct status')
    else:
      raise NotImplementedError(self.status)

    self.update(parrent)
    print('\r\033[K', end='')
    print(self.__str__(prefix, last_prefix, reclusive=False, skip=action == Action.SKIP))

    self.create_children(parrent, action, prefix, last_prefix, **kwargs)
    return action

  def create_element(self, path : pathlib.Path, **kwargs):
    raise NotImplementedError()

  def create_children(self, parrent : str = '', action : Action = Action.COMPLET, prefix : str = '', last_prefix : str = '', **kwargs):
    pass

  def __str__(self, **kwargs) -> str:
    color = '\033[90m' if kwargs.get('skip', False) else self.status.color
    icon = '→' if kwargs.get('skip', False) else self.status.icon
    return f'{color}{self.name} {icon}\033[0m'

  @staticmethod
  def normalize_name(name : str) -> str:
    return name if name and name[-1] != '/' else name[:-1]

  @staticmethod
  def remove(path : pathlib.Path):
    if not path.exists():
      return
    if path.is_dir():
      path.rmdir()
    else:
      path.unlink()

  @staticmethod
  def from_HTML(doc : BeautifulSoup):
    from .file import File
    from .folder import Folder

    name_html = doc.findChild()
    name : str = (name_html if name_html else doc).get_text()
    if not name:
      raise ValueError('name c\'ant be null')
    sub_struct : BeautifulSoup = doc.find('ul')

    if sub_struct:
      try:
        children : List[Struct] = [ Struct.from_HTML(child) for child in sub_struct.findChildren(recursive=False) ]
      except ValueError as e:
        raise ValueError(f"{name}/{e}")
      else:
        return Folder(name, children)
    elif name.endswith('/'):
      return Folder(name)
    else:
      return File(name)