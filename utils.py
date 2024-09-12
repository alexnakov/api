def find_value_in_dict(data, target_key):
    # If the current data is a dictionary, iterate over it
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            elif isinstance(value, (dict, list)):
                result = find_value_in_dict(value, target_key)
                if result is not None:
                    return result
    # If the current data is a list, iterate over the list
    elif isinstance(data, list):
        for item in data:
            result = find_value_in_dict(item, target_key)
            if result is not None:
                return result
    # If the key is not found, return None
    return None
