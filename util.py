import math


def max_list(source_list, key_func):
    results = []
    largest = -math.inf
    for item in source_list:
        key = key_func(item)
        if key > largest:
            largest = key
            results = [item]
        elif key == largest:
            results.append(item)

    return results
