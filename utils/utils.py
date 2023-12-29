import re

def preprocess_code(code):
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*', '', code)
    return code

def detect_loops(code):
    code = preprocess_code(code)
    lines = code.split('\n')

    loops = []
    current_indent = 0
    indent_stack = []

    for line in lines:
        line = line.strip()


        if '{' in line:
            indent_stack.append('{')
            current_indent = len(indent_stack) - 1


        match_for = re.match(r'\s*for\s*\((.*)\)\s*{?', line)
        match_while = re.match(r'\s*while\s*\((.*)\)\s*{?', line)

        if match_for or match_while:
            loop_type = 'for' if match_for else 'while'
            condition = match_for.group(1) if match_for else match_while.group(1)
            loop = {'type': loop_type, 'condition': condition, 'indent': current_indent}
            loops.append(loop)


        if '}' in line:
            if indent_stack and indent_stack[-1] == '{':
                indent_stack.pop()
            current_indent = len(indent_stack) - 1

    return loops

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
    code = preprocess_code(code)

    potential_function_lines = [
        line for line in code.split('\n') if re.match(r'\s*[a-zA-Z_]\w*\s+[a-zA-Z_]\w*\s*\([^)]*\)\s*{?', line)
        and not re.match(r'\s*(if|else if|else)\s*\(', line)
    ]

    function_names = []
    for line in potential_function_lines:
        match = re.match(r'\s*[a-zA-Z_]\w*\s+([a-zA-Z_]\w*)\s*\([^)]*\)\s*{?', line)
        if match:
            function_names.append(match.group(1))
    return function_names

def count_function_calls(code_content, function_name):
    pattern = re.compile(r'\b' + re.escape(function_name) + r'\s*\(')
    matches = pattern.findall(code_content)
    return len(matches)-1

def detect_conditions(code):
    code = preprocess_code(code)
    condition_lines = [line.strip() for line in code.split('\n') if re.match(r'\s*if\s*\(|\s*else if\s*\(|\s*else\s*{?', line)]
    
    conditions = []
    for line in condition_lines:
        match_if = re.match(r'\s*if\s*\((.*)\)\s*{?', line)
        match_elif = re.match(r'\s*else if\s*\((.*)\)\s*{?', line)
        match_else = re.match(r'\s*else\s*{?', line)

        if match_if:
            condition = {'type': 'if', 'condition': match_if.group(1)}
            conditions.append(condition)
        elif match_elif:
            condition = {'type': 'elif', 'condition': match_elif.group(1)}
            conditions.append(condition)
        elif match_else:
            condition = {'type': 'else', 'condition': None}
            conditions.append(condition)

    return conditions