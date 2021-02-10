import sys
import os
import argparse
import shutil
from enum import Enum

from function import init_call

__version__ = '1.1.0'

def nb_start_space(s : str) -> int:
  """
  get the number of space at the start

  :param s: the string to count space

  :return: the number of space at the start of `s`
  """
  length = len(s)
  for i in range(length):
    if s[i] != ' ':
      return i
  return length


def inputs(message : str) -> str:
  """
  get multiline user input

  :return: the multiline string of the user inputs
  """
  print(message)
  lines = ''
  line = ''
  while line or not lines:
    line = input()
    if line:
      lines += line +'\n'
  return lines

def struct_to_paths(root : str, data : str, tabsize : int = 4) -> list:
  """
  create paths from a html list architecture

  :param root: path to the root folder
  :param struct: a list of file indented by `tabsize` spaces
  :param tabsize: the number space composing 1 indentation

  :return: the list of path to create
  """
  if root[-1] != '/':
    root += '/'

  paths = []
  path = [root]
  for element in data:
    deep = nb_start_space(element) // tabsize
    path = path[:deep] + [element[deep * tabsize:]]
    paths.append(''.join(path))

  return paths

def is_sub_path(paths: list, path: str) -> bool:
  for blacklist_path in paths:
    if path.startswith(blacklist_path):
      return True
  return False

"""
✔
∅
⚠
✘
"""

def create_paths(paths : list, verbose : bool = False):
  """
  create files and folder from a list of path

  :param paths: list of the paths to create, forlder begin end with a "/"
  """
  backlist = []
  for path in paths:
    status = path_type(path)
    isdir, normalize_path = get_normalize_path(path)

    if is_sub_path(backlist, path):
      if verbose:
        print('\033[33;1m⚠ \033[21m' + path)
    elif status == FileStatus.EXIST or status == FileStatus.EMPTY:
      if verbose:
        print('\033[90;1m→ \033[21m' + path)
    elif status == FileStatus.WONG_TYPE:
      if overwrite_message(path):
        if isdir:
          os.remove(normalize_path)
        else:
          shutil.rmtree(normalize_path, ignore_errors=True)
        status = FileStatus.NOT_EXIST
      else:
        backlist.append(path)
        if verbose:
          print('\033[31;1m✘ \033[21m' + path)
    if status == FileStatus.NOT_EXIST:
      create_file_dir(isdir, path)
      if verbose:
        print('\033[32;1m✔ \033[21m' + path)


def overwrite_message(path: str) -> bool:
  response = 'soso'
  while response not in ['yes', 'y', 'no', 'n', '']:
    print(f'\033[0m"{path}" is of the wong type.')
    response = input('Did you want overwrite it ? (\033[4mYes\033[0m/No): ').lower()
    for i in range(2):
      print('\033[1A\r\033[K', end='')
  return response != 'no' and response != 'n'

def create_file_dir(isdir: bool, path : str):
  if isdir:
    os.makedirs(path)
  else:
    open(path, 'w+')

def get_data(file_path : str) -> str:
  data = ''
  if not file_path:
    data = inputs("Enter the project structure :").splitlines()
  else:
    with open(file_path, 'r') as f:
      data = [line[:-1] for line in f.readlines()]
  return [path for path in data if path]

class FileStatus(Enum):
  EXIST = 0
  EMPTY = 1
  WONG_TYPE = 2
  NOT_EXIST = 3


def catorize_paths(paths: list) -> dict:
  catorize = {
    FileStatus.EXIST: [],
    FileStatus.NOT_EXIST: [],
    FileStatus.WONG_TYPE: [],
    FileStatus.EMPTY: [],
  }
  for path in paths:
    status = path_type(path)
    catorize[status].append(path)
  return catorize

status_header = {
  FileStatus.EXIST: '\033[32;1m✔ %i Exist',
  FileStatus.EMPTY: '\033[34;1m∅ %i Empty file',
  FileStatus.WONG_TYPE: '\033[33;1m⚠ %i Wong type',
  FileStatus.NOT_EXIST: '\033[31;1m✘ %i Not exist',
}
file_prefix = {
  FileStatus.EXIST: '\033[0;32m %s',
  FileStatus.EMPTY: '\033[0;34m %s',
  FileStatus.WONG_TYPE: '\033[0;33m %s',
  FileStatus.NOT_EXIST: '\033[0;31m %s',
}

def is_valid_archi(categorizes: dict, args: dict) -> bool:
  if categorizes[FileStatus.NOT_EXIST]:
    return False
  if categorizes[FileStatus.WONG_TYPE]:
    return False
  if args.empty and categorizes[FileStatus.EMPTY]:
    return False
  return True

def get_normalize_path(path : str):
  isdir = path[-1] == '/'
  return (isdir, path[:-1] if isdir else path)


def path_type(path : str):
  """
  return if the file exist and if it is the good type
  """
  isdir, path = get_normalize_path(path)

  if not os.path.exists(path):
    return FileStatus.NOT_EXIST

  if isdir:
    return FileStatus.EXIST if os.path.isdir(path) else FileStatus.WONG_TYPE
  else:
    if os.path.isfile(path):
      return FileStatus.EXIST if os.stat(path).st_size else FileStatus.EMPTY
    else:
      return FileStatus.WONG_TYPE


def boxText(message : str, width : int, color : int, marge : int = 4):
  line_width = width - 2 * marge
  if line_width < 0:
    line_width = width
    marge = 0
  lines = message.splitlines()
  box_lines = []
  for line in lines:
    box_lines += [line[i:i + line_width] for i in range(0, len(line), line_width)]

  bankline = ' ' * width
  print(f'\033[0;1;{color};7m', end='')
  for i in range(marge // 2):
    print(bankline)
  for line in box_lines:
    space_len = (width - len(line)) // 2
    space_marge = ' ' * space_len
    if space_len & 1:
      print(' ', end='')
    print(space_marge + line + space_marge)
  for i in range(marge // 2):
    print(bankline)

def check(args):
  data = get_data(args.file)
  paths = struct_to_paths(args.root ,data)
  categorizes = catorize_paths(paths)

  #if args.all:
    #args.list = True

  if args.verbose:
    args.count = True
    args.list = True
    args.all = True

  if not args.empty and not args.all:
    categorizes[FileStatus.EXIST] += categorizes[FileStatus.EMPTY]
    categorizes[FileStatus.EMPTY] = []

  if is_valid_archi(categorizes, args):
    boxText('VALID ARCHI', 50, 32)
    # print('\033[0;1;32;7m'+ ' ' * 24 +'                 \n   VALID ARCHI   \n                 ')
  else:
    boxText('FAIL ARCHI', 50, 31)
    # print('\033[0;1;31;7m                \n   FAIL ARCHI   \n                ')

    #print(f'\033[0;1;31mFAIL ARCHI')
  print(f'\033[0m')

  for status in FileStatus:
    paths = categorizes[status]
    if not paths and not args.all:
      continue
    if args.count:
      print(status_header[status] % len(paths))

    if not args.list:
      continue

    for path in paths:
      print(file_prefix[status] % path)
    print(f'\033[0m')



def export(args):
  print('export', args)



def apply(args):
  data = get_data(args.file)
  paths = struct_to_paths(args.root ,data)
  create_paths(paths, args.verbose)

  #print(subject.get_text())
  #git_url = get_git_url(subject)

def version(args):
  print(f'Fail archi v{__version__}')
  if args.verbose:
    print('\nFail archi is a litle program to create check')
    print('and export project architectur')
    print('\nby Jules Lefebvre <jules.lefebvre@epita.fr>')


def main():
  parser = argparse.ArgumentParser(
    add_help=False,
    description='Fail archi is a litle program to create check and export project architecture'
  )
  parser.set_defaults(func=lambda args: parser.print_help())
  optional_group = parser.add_argument_group('optional arguments')
  optional_group.add_argument('-h', '--help', action='help', help='show this help message and exit')
  optional_group.add_argument('-v', '--verbose', help='output verbosity', action='count')
  optional_group.add_argument('--version', action='version', version=f'Fail archi v{__version__} by Jules Lefebvre <jules.lefebvre@epita.fr>')

  command_parser  = parser.add_subparsers(title='command', help='command to execute')

  parser_apply = command_parser.add_parser('apply', help='create the architecture')
  parser_apply.set_defaults(func=apply)
  parser_apply.add_argument( 'root', help='the path of the root the architecture', type=str, default='./', nargs='?')
  parser_apply.add_argument('-f', '--file', help='path of a input structur file', type=str)
  parser_apply.add_argument('-v', '--verbose', help='all the print parameter', action='store_true')

  parser_check = command_parser.add_parser('check', help='check if the the architecture is comform')
  parser_check.set_defaults(func=check)
  parser_check.add_argument( 'root', help='the path of the root of the architecture', type=str, default='./', nargs='?')
  parser_check.add_argument('-f', '--file', help='path of a input structur file', type=str)
  parser_check.add_argument('-v', '--verbose', help='all the print parameter', action='store_true')
  parser_check.add_argument('-c', '--count', help='show file/folder count', action='store_true')
  parser_check.add_argument('-l', '--list', help='print all paths', action='store_true')
  parser_check.add_argument('-a', '--all', help='print all type of paths', action='store_true')
  parser_check.add_argument('-e', '--empty', help='check for empty file', action='store_true')

  parser_init = command_parser.add_parser('init', help='clone and create architecture from page')
  parser_init.set_defaults(func=init_call)
  parser_init.add_argument('root', help='the path of the root of the architecture', type=str, default='', nargs='?')
  parser_init.add_argument('url', help='url of the subject', type=str)

  parser_export = command_parser.add_parser('export', help='export the architecture')
  parser_export.set_defaults(func=export)

  args = parser.parse_args()
  args.func(args)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Aborded')