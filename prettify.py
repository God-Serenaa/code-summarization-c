def pretty_print(function_details):
  for function in function_details:
    print(f"function name: {function['name']}")

    print(f"this function was called {function['call_count']} times")

    print(f"condition count: {function['condition_count']}")
    for condition in function['conditions']:
        print(f"\tType: {condition['type']}, Condition: {condition['condition']}")

    print(f"loop count; {function['loop_count']}")
    ind = 0
    for loop in function['loops']:
        ind = max(ind, loop['indent'])
        print(f"\tType: {loop['type']}, Condition: {loop['condition']}, Indent: {loop['indent']}")

    print(f"Time complexity: {'1' if ind == 0 else 'n^'+str(ind)}")
    print("\n\n")