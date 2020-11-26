positive_answer = ['yes', 'y', '']
negative_answer = ['no', 'n']

def choice_message(message : str) -> bool:
  response = 'a'
  while response not in positive_answer and response not in negative_answer:
    response = input(message + ' (\033[4mYes\033[0m/No): ').lower()
    for i in range(2):
      print('\033[1A\r\033[K', end='')
  return response in positive_answer


def remove_indent(file : str) -> str:
  def get_indent(s : str) -> int:
    for i, c in enumerate(s):
      if c != ' ':
        return i
    return None

  lines = file.splitlines()
  min_indent = None

  for line in lines:
    indent : int = get_indent(line)
    if min_indent == None:
      min_indent = indent
    if indent != None and min_indent > indent:
      min_indent = indent

  out = ''
  for line in lines:
    out += line[min_indent:] + '\n'

  return out.strip()