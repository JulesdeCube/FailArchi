from bs4 import BeautifulSoup
import urllib.request
import re
import pathlib

import settings
from git import Repo, Git, GitCommandError
from archi import Struct, Folder, File
from utils import remove_indent

from archi.action import Action

def init_call(args):
  path : str = args.root
  subject = get_subject(args.url)
  if args.verbose:
    print(f"\033[1;32m✔\033[0m fetch subject from \033[90m{args.url}\033[0m")

  git_url_patern = get_git(subject.get_text())
  if args.verbose:
    print(f"\033[1;32m✔\033[0m get repository url patern : \033[90m{git_url_patern}\033[0m")

  git_url = replace_usernaname(git_url_patern, settings.LOGIN)
  print("\033[1;32m✔\033[0m get repository url", end='')
  if args.verbose:
    print(f" : \033[90m{git_url}\033[0m")
  else:
    print()

  if not path:
    path = re.findall(r'([^/\\]+)(.git)?$', git_url)[0][0]

  struct : Folder = get_struct(subject, path)
  print(f"\033[1;32m✔\033[0m structur parsed")

  files = get_files(subject)
  if args.verbose:
    print(f"\033[1;32m✔\033[0m {len(files)} files founds :")
    for file in files:
      print(f'- \033[90m{file}\033[0m')


  git_clone(git_url, path)
  print(f"\033[1;32m✔\033[0m clone repository")

  status = struct.create(files = files, verbose=args.verbose)
  print(f"{status.color}{status.icon}\033[0m create project structure")


def get_subject(url : str) -> BeautifulSoup:
  try:
    fp = urllib.request.urlopen(url)
  except urllib.request.HTTPError as e:
    print(f"\033[1;31m✘ ERROR:\033[0m durring subject download ({e})")
    exit(1)
  except (ValueError, urllib.request.URLError) as e:
    print(f"\033[1;31m✘ ERROR:\033[0m {e}")
    exit(1)
  else:
    subject_html = fp.read().decode("utf8")
    fp.close()
    return BeautifulSoup(subject_html, features="html.parser")

def get_git(text: str) -> str:
  urls = [path[0] for path in re.findall('((\w+://)?([\w.]+@)?[\w.]+\.[a-z]{2,}:[a-zA-Z0-9._/-]+)', text)]
  if not len(urls):
    print(f"\033[1;31m✘ ERROR:\033[0m no git repository found")
    exit(1)
  url = urls[0]
  # TODO
  return url

def replace_usernaname(url : str, username : str) -> str:
  for patern in ['john.smith', 'nom.prenom', 'username', 'login']:
    url = url.replace(patern, username)
  return url

def git_clone(url : str, path : str):
  try:
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
  except FileExistsError as e:
    print(f"\033[1;31m✘ ERROR:\033[0m can't create root folder \033[90m{path}\033[0m ({e})")
    exit(1)
  try:
    if path:
     Repo.clone_from(url, path)
  except GitCommandError as e:
    print(f"\033[1;31m✘ ERROR:\033[0m can't clone repository ({e.stderr[:-1].strip()})")
    exit(1)

def get_struct(subject : BeautifulSoup, root : str) -> Folder:
  struct_root : BeautifulSoup = subject.find('ul')
  if not struct_root:
    print(f"\033[1;31m✘ ERROR:\033[0m can't find the structure")
    exit(1)

  try:
    struct = Folder(root, [Struct.from_HTML(child) for child in struct_root.findChildren(recursive=False)])
  except ValueError as e:
    print(f"\033[1;31m✘ ERROR:\033[0m can't create structure : {e}")
    exit(1)
  else:
    if not '.gitingore' in struct:
      struct.children.append(File('.gitignore'))

  return struct

def get_files(subject : BeautifulSoup) -> Folder:
  files = {}
  for filename_html in subject.findAll('div', class_ = 'filename'):
    filename : str = filename_html.get_text().strip()
    code_text : str = filename_html.findNextSibling().get_text()
    code : str = remove_indent(code_text)
    files[filename] = code

  return files
