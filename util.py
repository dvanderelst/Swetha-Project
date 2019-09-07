def match_variables(data, variables):
    names = list(data.columns)
    if not isinstance(variables, (list, tuple)): variables = [variables]
    variables_lower = list2lower(variables)
    names_lower = list2lower(names)
    matched_variables = []
    failed_variables = []
    for lower, original in zip(variables_lower, variables):
        try:
            index = names_lower.index(lower)
            matched = names[index]
            matched_variables.append(matched)
        except:
            failed_variables.append(original)
    return matched_variables, failed_variables


def list2lower(lst):
    result = [x.lower() for x in lst]
    return result


def name_range(base, n):
    names = []
    for x in range(0, n): names.append(base + str(x))
    return names


def normalize(value, min_value, max_value):
    delta = max_value - min_value
    new = value - min_value
    new = new / delta
    if new < 0: new = 0
    if new > 1: new = 1
    return new
