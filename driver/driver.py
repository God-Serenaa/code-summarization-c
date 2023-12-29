from utils.utils import preprocess_code, detect_loops, detect_conditions

def driver(PATH):
  with open(PATH) as f:
    code_lines = f.readlines()

    code = ''
    for line in code_lines:
      code += "\n"+line

    code_string = preprocess_code(code)

    loops = detect_loops(code_string)
    loop_count = len(loops)

    conditions = detect_conditions(code_string)
    conditions_count = len(conditions)

    return (loops, loop_count, conditions, conditions_count)