def change_string_with_numbers_to_int(string_with_numbers):
    """
    Changes string that contain numbers to int value.
    :param string_with_numbers: <str> -> string containing numbers
    :return: <int> -> integer value of numbers from string
    """
    return int(''.join([x for x in string_with_numbers if x.isdigit()]))
