import re

def preprocess_code(code):
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*', '', code)
    return code

def count_brackets(line):
    opening_brackets = re.findall(r'{', line)
    closing_brackets = re.findall(r'}', line)
    return len(opening_brackets), len(closing_brackets)

def extract_function(function, code):
  declarations = [f"{i} {function}" for i in ['int', 'bool', 'float', 'double', 'void']]
  flag = False
  opening_count = 0
  closing_count = 0
  function_code = """"""
  for line in code:
    if not flag:
      for declaration in declarations:
        if declaration in line:
          flag=True
          o, c = count_brackets(line)
          opening_count += o
          closing_count += c

          function_code += line
          break
    else:
      o, c = count_brackets(line)
      opening_count += o
      closing_count += c

      function_code += line
    if opening_count !=0 and opening_count == closing_count:
      return {"name": function, "body": function_code}

def detect_functions(code):
    potential_function_lines = [
        line for line in code.split('\n') if re.match(r'\s*[a-zA-Z_]\w*\s+[a-zA-Z_]\w*\s*\([^)]*\)\s*{?', line)
    ]
    potential_function_lines = [
        line for line in potential_function_lines if not re.match(r'\s*(if|else if|else)\s*\(', line)
    ]

    function_names = []
    for line in potential_function_lines:
        match = re.match(r'\s*[a-zA-Z_]\w*\s+([a-zA-Z_]\w*)\s*\([^)]*\)\s*{?', line)
        if match:
            function_names.append(match.group(1))
    return function_names