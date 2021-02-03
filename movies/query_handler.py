from awards_counter import AwardsCounter
from database import DatabaseHandler
from utils import change_string_with_numbers_to_int


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
        return any(char.isdigit() for char in string)

    def prepare_value_to_sort(self, value):
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

    def sort_movies_data_by_table_names_decreasing(self, list_of_movies, table_names):
        """
        Sorts list of tuples without the first one tuple which is title of the movie.
        :param list_of_movies: <list> -> list of database objects - movies
        :param table_names: <tuple> -> argument(s) from script
        :return: <list> -> sorted list of database objects - movies
        """
        return sorted(list_of_movies, key=lambda x: [(self.prepare_value_to_sort(str(x[table_name])) if x != 'N/A' else
                                                      str(0)) for table_name in table_names], reverse=True)

    def get_data_to_sort(self):
        """
        Gets data to sort by table names from the database.
        :return: <list> -> prepared list of tuples of data for sorting
        """
        return [movie for movie in self.get_all()]

    def sort_by_selected_table_names(self, table_names):
        """
        Sorts data from database by table names entered as a script arguments.
        :param table_names: <tuple> -> argument(s) from script
        :return: <list> -> sorted list of tuples
        """
        return [tuple([movie['title']] + [movie[table_name] for table_name in table_names]) for movie in
                self.sort_movies_data_by_table_names_decreasing(self.get_data_to_sort(), table_names)]


class FilterByHandler(QueryHandler):
    """Inheriting class for initialize empty list of filtered movie which will be filled."""

    def __init__(self):
        super().__init__()
        self.filtered_movies = []


class FilterByValueHandler(FilterByHandler):
    """Inheriting class storing methods to get filtered movies by entered table name and value."""

    def get_filtered_movies_by_value(self, table_name, value):
        """
        Gets filtered movies by entered table name and value.
        :param table_name: <str> -> database table name
        :param value: <str> -> the value by which the data is filtered
        :return: <list> -> list of tuples with filtered movies data.
        """
        self.filter_movies_by_value(table_name, value)
        return [(movie['title'], movie[table_name]) for movie in self.filtered_movies]

    def filter_movies_by_value(self, table_name, value):
        """
        Filters movies by entered table name and value.
        :param table_name: <str> -> database table name
        :param value: <str> -> the value by which the data is filtered
        """
        self.filtered_movies = list(
            filter(lambda movie: value.lower() in str(movie[table_name]).lower().split(), self.get_all()))


class FilterByNominatedForOscar(FilterByHandler):
    """Inheriting class storing methods to get filtered movies that which were nominated for oscar and have not won."""

    def get_filtered_movies_by_nomination_for_oscar(self):
        """Gets filtered list of movies.
        :return: <list> -> list of tuples with filtered movie data
        """
        self.filter_movies_by_nomination_for_oscar()
        return self.filtered_movies

    def check_nomination_for_oscar(self, movie, movie_with_awards):
        """
        Checks if movie has nomination for oscar and have not won any of them.
        :param movie: <sqlite3.Row> -> database movie data
        :param movie_with_awards: <awards_counter.AwardsCounter> -> awards counter object
        """
        if movie_with_awards.oscars_wins == 0 and movie_with_awards.oscars_nominations > 0:
            self.filtered_movies.append((movie['title'], movie['awards']))

    def filter_movies_by_nomination_for_oscar(self):
        """
        Filter movies that has nomination for oscar and have not won any.
        """
        for movie in self.get_all():
            temp_awards_counter = AwardsCounter(movie)
            temp_awards_counter.scrape_awards()
            self.check_nomination_for_oscar(movie, temp_awards_counter)


class FilterByWinsNominations(FilterByHandler):
    """Inheriting class storing methods to get filtered movies which has more wins than 80% of nominations."""

    def get_filtered_movies_by_wins_nominations(self):
        """
        Gets filtered movies.
        :return: <list> -> list of tuples with filtered movie data
        """
        self.filter_movies_by_wins_nominations()
        return self.filtered_movies

    def check_wins_nominations(self, movie, movie_with_awards):
        """
        Checks if movie has more wins than 80% of nominations.
        :param movie: <sqlite3.Row> -> database movie data
        :param movie_with_awards: <awards_counter.AwardsCounter> -> awards counter object
        """
        if movie_with_awards.wins + movie_with_awards.oscars_wins > 0.8 * \
                (movie_with_awards.nominations + movie_with_awards.oscars_nominations):
            self.filtered_movies.append((movie['title'], movie['awards']))

    def filter_movies_by_wins_nominations(self):
        """Filters movies which has more wins than 80% of nominations."""
        for movie in self.get_all():
            temp_awards_counter = AwardsCounter(movie)
            temp_awards_counter.scrape_awards()
            self.check_wins_nominations(movie, temp_awards_counter)


class FilterByBoxOffice(FilterByHandler):
    """Inheriting class storing methods to filter movies which box office is larger than 100.000.000$."""

    def get_filtered_movies_by_box_office(self):
        """
        Gets filtered movies.
        :return: <list> -> list of tuples with filtered movie data
        """
        self.filter_movies_by_box_office()
        return [(movie['title'], movie['box_office']) for movie in self.filtered_movies]

    def filter_movies_by_box_office(self):
        """Filter movies which box office is larger than 100.000.000$."""
        self.filtered_movies = list(filter(lambda movie: (change_string_with_numbers_to_int(
            movie['box_office']) if movie['box_office'] != 'N/A' else 0) > 100000000, self.get_all()))
