from utils.utils import preprocess_code, detect_functions, extract_function

def driver(PATH):
  with open(PATH) as f:
    code_lines = f.readlines()

    code = ''
    for line in code_lines:
      code += "\n"+line
    
    code_string = preprocess_code(code)
    functions = detect_functions(code_string)

    function_info = []
    for function in functions:
      temp = extract_function(function, code_lines)
      function_info.append({"name": function, "body": temp})
    
    return function_info