from utils.utils import preprocess_code, detect_functions, extract_function, count_function_calls

def driver(PATH):
  with open(PATH) as f:
    code_lines = f.readlines()

    code = ''
    for line in code_lines:
      code += "\n"+line

    code_string = preprocess_code(code)
    functions = detect_functions(code_string)
    
    function_call = []
    for function in functions:
      temp = {"name": function}
      temp["call_count"] = count_function_calls(code, function)
      function_call.append(temp)
    
    return function_call