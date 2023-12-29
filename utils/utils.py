import re

def preprocess_code(code):
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*', '', code)
    return code

def detect_loops(code):
    code = preprocess_code(code)
    lines = code.split('\n')

    loops = []
    current_indent = 0  # Track the current nesting level
    indent_stack = []  # Stack to manage indent levels

    for line in lines:
        line = line.strip()

        # Increase indent level when a '{' is found
        if '{' in line:
            indent_stack.append('{')
            current_indent = len(indent_stack) - 1

        # Detect 'for' and 'while' loops
        match_for = re.match(r'\s*for\s*\((.*)\)\s*{?', line)
        match_while = re.match(r'\s*while\s*\((.*)\)\s*{?', line)

        if match_for or match_while:
            loop_type = 'for' if match_for else 'while'
            condition = match_for.group(1) if match_for else match_while.group(1)
            loop = {'type': loop_type, 'condition': condition, 'indent': current_indent}
            loops.append(loop)

        # Decrease indent level when a '}' is found
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

def count_function_calls(code_content, function_name):
    pattern = re.compile(r'\b' + re.escape(function_name) + r'\s*\(')
    matches = pattern.findall(code_content)
    return len(matches)-1