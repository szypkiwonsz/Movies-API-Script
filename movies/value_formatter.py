from utils import change_string_with_numbers_to_int


class ValueFormatter:
    """Class storing methods formatting the value to prepare it for sorting or comparison."""

    @staticmethod
    def is_award_value(value):
        """
        Checks if entered value is movie award value.
        :param value: <str> -> movie value
        :return: <bool> -> True if value is value of movie award, False if not
        """
        award_keywords = ['Nominated', 'nomination.', 'nominations.', 'wins', 'Won']
        return True if any(word in str(value) for word in award_keywords) else False

    @staticmethod
    def is_float_value(value):
        """
        Checks if entered value is an imdb rating movie value.
        :param value: <str> -> movie value
        :return: <bool> -> False if the value is not an imdb rating movie value, True if it is
        """
        return isinstance(value, float)

    @staticmethod
    def has_digit(string):
        """
        Checks if entered string has a digit.
        :param string: <str> -> string with or without digit
        :return: <bool> -> True if string has a digit, False if not
        """
        return any(char.isdigit() for char in str(string))

    def prepare_value(self, value):
        """
        A helper function for preparing value to sort with lambda.
        :param value: <str> -> movie value from database
        :return: <int> -> sum of numbers if value is an award value, <int> -> if value has digit and is not an imdb
        rating value, <string> -> if neither of the previous ones
        """
        if self.is_award_value(value):
            return sum([int(x) for x in [x for x in value.split() if x.isdigit()]])
        elif self.has_digit(value) and not self.is_float_value(value):
            return change_string_with_numbers_to_int(value)
        else:
            return value
