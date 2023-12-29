from utils.utils import preprocess_code, detect_loops, detect_conditions, detect_functions, extract_function, count_function_calls
def driver(PATH):
    with open(PATH) as f:
        code_lines = f.readlines()

        code = ''
        for line in code_lines:
            code += "\n"+line

        code_string = preprocess_code(code)
        functions = detect_functions(code_string)

        function_details = []
        for function in functions:
            temp = extract_function(function, code_lines)
            temp["call_count"] = count_function_calls(code_string, function)

            temp["conditions"] = detect_conditions(temp["body"])
            temp["condition_count"] = len(temp["conditions"])

            temp["loops"] = detect_loops(temp["body"])
            temp["loop_count"] = len(temp["loops"])

            function_details.append(temp)
    
    return function_details