from database import DatabaseHandler


class QueryHandler(DatabaseHandler):
    """Class storing methods for basics database queries."""

    def get_all(self):
        """
        Gets all data about movies from database.
        :return: <list> -> movies data
        """
        return self.cur.execute(f'SELECT * FROM MOVIES').fetchall()

    def get_all_titles(self):
        return [movie['title'] for movie in self.get_all()]


class SortByValuesHandler(QueryHandler):
    """Class storing methods for sorting data about movies from database."""

    @staticmethod
    def is_award_value(value):
        """
        Checks if entered value is movie award value.
        :param value: <str> -> movie value
        :return: <bool> -> True if value is value of movie award, False if not
        """
        award_keywords = ['Nominated', 'nomination.', 'nominations.', 'wins', 'Won']
        return True if any(word in value for word in award_keywords) else False

    @staticmethod
    def clean_value_to_sort(value):
        """
        Cleans movie value needed for proper sorting.
        param value: <str> -> value to clean
        return: <str> -> cleaned value
        """
        return clean_box_office_value(value)

    @staticmethod
    def is_imdb_rating_value(value):
        """
        Checks if entered value is an imdb rating movie value.
        :param value: <str> -> movie value
        :return: <bool> -> False if the value is not an imdb rating movie value, True if it is
        """
        return False if [x for x in value.split() if x.isdigit()] else True

    @staticmethod
    def has_digit(string):
        """
        Checks if entered string has a digit.
        :param string: <str> -> string with or without digit
        :return: <bool> -> True if string has a digit, False if not
        """
        return any(char.isdigit() for char in string)

    def sort_by_type(self, value):
        """
        A helper function for sorting with lambda.
        :return: <int> -> sum of numbers if value is an award value, <int> -> if value has digit and is not an imdb
        rating value, <string> -> if neither of the previous ones
        """
        if self.is_award_value(value):
            return sum([int(x) for x in [x for x in value.split() if x.isdigit()]])
        elif self.has_digit(value) and not self.is_float_value(value):
            return change_string_with_numbers_to_int(value)
        else:
            return value

    def sort_list_decreasing(self, list_to_sort):
        """
        Sorts list of tuples without the first one tuple which is title of the movie.
        :param list_to_sort: <list> -> list of tuples to be sorted
        :return: <list> -> sorted list of tuples
        """
        return sorted(list_to_sort, key=lambda x: [self.sort_by_type(
            str(x) if x != 'N/A' else str(0)) for x in x[1:]], reverse=True)

    def get_data_to_sort(self, table_names):
        """
        Gets data to sort by table names from the database.
        :param table_names: <tuple> -> names of tables against which the data will be sorted
        :return: <list> -> prepared list of tuples of data for sorting
        """
        return [[movie['title']] + [movie[table] for table in table_names] for movie in self.get_all()]

    def sort_by_selected_table_names(self, table_names):
        """
        Sorts data from database by table names entered as a script arguments.
        :param table_names: <tuple> -> argument(s) from script
        :return: <list> -> sorted list of tuples
        """
        return self.sort_list_decreasing(self.list_of_lists_to_tuples(self.get_data_to_sort(table_names)))

    @staticmethod
    def list_of_lists_to_tuples(list_of_lists):
        """
        Changes list of lists to list of tuples.
        :param list_of_lists: <list> -> list of lists
        :return: <list> -> list of tuples
        """
        return [tuple(element) for element in list_of_lists]
