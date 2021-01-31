def clean_box_office_value(value):
    """
    Cleans movie value needed for proper sorting box office values.
    :param value: <str> -> movie value
    :return: <str> -> string contains only numbers
    """
    value = value.replace(',', '')
    value = value.replace('$', '')
    return value
