from utils.utils import preprocess_code

def driver(PATH):
  with open(PATH) as f:
    code_lines = f.readlines()

    code = ''
    for line in code_lines:
      code += "\n"+line

    code_string = preprocess_code(code)
    return code_string