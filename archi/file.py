import pathlib

import settings
from .struct import Struct
from .state import State
from .action import Action
from utils import choice_message

class File(Struct):

  icon : dict = {
    'authors' : '👥',
    'makefile' : '🧰',
    '.gitignore': '🙈',
  }

  default_files = {}

  overwrite_files = {
    'AUTHORS':
      f'{settings.FIRSTNAME}\n'
      f'{settings.LASTNAME}\n'
      f'{settings.LOGIN}\n'
      f'{settings.LOGIN}@epita.fr\n'
  }

  def get_icon(self):
    return self.icon.get(self.name.lower(), '📄')

  def __str__(self, prefix : str = '', last_prefix : bool = '', **kwargs : dict) -> str:
    return prefix + last_prefix + self.get_icon() +  super().__str__(**kwargs)

  def type_check(self, path : pathlib.Path) -> bool:
    return path.is_file()

  def create_element(self, path : str = '', **kwargs):
    path.touch(exist_ok=True)
    code = self.get_code(kwargs.get('files', {}))
    with open(path, 'w') as f:
      f.write(code)

  def get_code(self, project_files):
    code = self.default_files.get(self.name, '')
    code = project_files.get(self.name, code)
    code = self.overwrite_files.get(self.name, code)
    try:
      code = settings.FILES.get(self.name, code)
    except AttributeError:
      pass
    return code