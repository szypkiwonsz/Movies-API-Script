from awards_counter import AwardsCounter
from database import DatabaseHandler
from utils import change_string_with_numbers_to_int
from value_formatter import ValueFormatter


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


class SortByValueHandler(QueryHandler, ValueFormatter):
    """Class storing methods for sorting data about movies from database."""

    def sort_movies_data_by_columns_decreasing(self, list_of_movies, columns):
        """
        Sorts list of tuples without the first one tuple which is title of the movie.
        :param list_of_movies: <list> -> list of database objects - movies
        :param columns: <tuple> -> argument(s) from script
        :return: <list> -> sorted list of database objects - movies
        """
        return sorted(list_of_movies, key=lambda x: [
            self.prepare_value(str(x[column]) if x[column] != 'N/A' else str(0)) for column in
            columns], reverse=True)

    def get_data_to_sort(self):
        """
        Gets data to sort by table names from the database.
        :return: <list> -> prepared list of tuples of data for sorting
        """
        return [movie for movie in self.get_all()]

    def sort_by_selected_columns(self, columns):
        """
        Sorts data from database by table names entered as a script arguments.
        :param columns: <tuple> -> argument(s) from script
        :return: <list> -> sorted list of tuples
        """
        return [tuple([movie['title']] + [movie[column] for column in columns]) for movie in
                self.sort_movies_data_by_columns_decreasing(self.get_data_to_sort(), columns)]


class FilterByHandler(QueryHandler):
    """Inheriting class for initialize empty list of filtered movie which will be filled."""

    def __init__(self):
        super().__init__()
        self.filtered_movies = []


class FilterByValueHandler(FilterByHandler):
    """Inheriting class storing methods to get filtered movies by entered table name and value."""

    def get_filtered_movies_by_value(self, column, value):
        """
        Gets filtered movies by entered table name and value.
        :param column: <str> -> database table name
        :param value: <str> -> the value by which the data is filtered
        :return: <list> -> list of tuples with filtered movies data.
        """
        self.filter_movies_by_value(column, value)
        return [(movie['title'], movie[column]) for movie in self.filtered_movies]

    def filter_movies_by_value(self, column, value):
        """
        Filters movies by entered table name and value.
        :param column: <str> -> database table name
        :param value: <str> -> the value by which the data is filtered
        """
        self.filtered_movies = list(
            filter(lambda movie: value.lower() in str(movie[column]).lower().split(), self.get_all()))


class FilterByNominatedForOscarHandler(FilterByHandler):
    """Inheriting class storing methods to get filtered movies that which were nominated for oscar and have not won."""

    def get_filtered_movies_by_nomination_for_oscar(self):
        """Gets filtered list of movies.
        :return: <list> -> list of tuples with filtered movie data
        """
        self.filter_movies_by_nomination_for_oscar()
        return self.filtered_movies

    def check_nomination_for_oscar(self, movie_with_awards):
        """
        Checks if movie has nomination for oscar and have not won any of them.
        :param movie_with_awards: <awards_counter.AwardsCounter> -> awards counter object
        """
        if movie_with_awards.oscars_wins == 0 and movie_with_awards.oscars_nominations > 0:
            self.filtered_movies.append((movie_with_awards.movie['title'], movie_with_awards.movie['awards']))

    def filter_movies_by_nomination_for_oscar(self):
        """
        Filter movies that has nomination for oscar and have not won any.
        """
        for movie in self.get_all():
            temp_awards_counter = AwardsCounter(movie)
            self.check_nomination_for_oscar(temp_awards_counter)


class FilterByWinsNominationsHandler(FilterByHandler):
    """Inheriting class storing methods to get filtered movies which has more wins than 80% of nominations."""

    def get_filtered_movies_by_wins_nominations(self):
        """
        Gets filtered movies.
        :return: <list> -> list of tuples with filtered movie data
        """
        self.filter_movies_by_wins_nominations()
        return self.filtered_movies

    def check_wins_nominations(self, movie_with_awards):
        """
        Checks if movie has more wins than 80% of nominations.
        :param movie_with_awards: <awards_counter.AwardsCounter> -> awards counter object
        """
        if movie_with_awards.wins + movie_with_awards.oscars_wins > 0.8 * \
                (movie_with_awards.nominations + movie_with_awards.oscars_nominations):
            self.filtered_movies.append((movie_with_awards.movie['title'], movie_with_awards.movie['awards']))

    def filter_movies_by_wins_nominations(self):
        """Filters movies which has more wins than 80% of nominations."""
        for movie in self.get_all():
            temp_awards_counter = AwardsCounter(movie)
            self.check_wins_nominations(temp_awards_counter)


class FilterByBoxOfficeHandler(FilterByHandler):
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


class CompareByValueHandler(QueryHandler, ValueFormatter):
    """Inheriting class storing methods for comparing two movies by selected value."""

    def __init__(self, column):
        super().__init__()
        self.column = column

    def compare_movies_by_value(self, first_movie, second_movie):
        """
        Compares two movies by value.
        :param first_movie: <sqlite3.Row> -> database object of first movie to compare
        :param second_movie: <sqlite3.Row> -> database object of second movie to compare
        :return: <sqlite3.Row> -> database movie object with higher compared value
        """
        return max([first_movie, second_movie], key=lambda x: self.prepare_value(x[self.column]))

    def get_compared_movie_by_value(self, first_movie, second_movie):
        """Gets compared movie by higher value.
        :param first_movie: <sqlite3.Row> -> database object of first movie to compare
        :param second_movie: <sqlite3.Row> -> database object of second movie to compare
        :return: <tuple> -> compared movie with higher value
        """
        movie = self.compare_movies_by_value(first_movie, second_movie)
        return movie['title'], movie[self.column]

    def get_movie_by_title(self, movie_title):
        """
        Gets movie database object by title.
        :param movie_title: <str> -> title of the movie
        :return: <str> -> movie database object
        """
        return [x for x in self.get_all() if x['title'] == movie_title][0]


class CompareByImdbRatingHandler(CompareByValueHandler):
    """Inheriting class storing methods do compare movies by imdb rating."""

    def __init__(self):
        super().__init__('IMDb_Rating')

    def get_compared_movies_by_imdb_rating(self, first_movie_title, second_movie_title):
        """
        Gets compared movies by imdb rating.
        :param first_movie_title: <str> -> first script argument (title of the movie)
        :param second_movie_title: <str> -> second script argument (title of the movie)
        :return: <tuple> -> compared movie with higher value
        """
        return self.get_compared_movie_by_value(self.get_movie_by_title(first_movie_title),
                                                self.get_movie_by_title(second_movie_title))


class CompareByBoxOfficeHandler(CompareByValueHandler):
    """Inheriting class storing methods do compare movies by box office."""

    def __init__(self):
        super().__init__('BOX_OFFICE')

    def get_compared_movies_by_box_office(self, first_movie_title, second_movie_title):
        """
        Gets compared movies by box office.
        :param first_movie_title: <str> -> first script argument (title of the movie)
        :param second_movie_title: <str> -> second script argument (title of the movie)
        :return: <tuple> -> compared movie with higher box office value
        """
        return self.get_compared_movie_by_value(self.get_movie_by_title(first_movie_title),
                                                self.get_movie_by_title(second_movie_title))


class CompareByAwardsWonHandler(CompareByValueHandler):
    """Inheriting class storing methods do compare movies by awards won."""

    def __init__(self):
        super().__init__('AWARDS')

    def get_compared_movies_by_awards_won(self, first_movie_title, second_movie_title):
        """
        Gets compared movies by awards won.
        :param first_movie_title: <str> -> first script argument (title of the movie)
        :param second_movie_title: <str> -> second script argument (title of the movie)
        :return: <tuple> -> compared movie with more awards won
        """
        return self.get_compared_movie_by_value(self.get_movie_by_title(first_movie_title),
                                                self.get_movie_by_title(second_movie_title))


class CompareByRuntimeHandler(CompareByValueHandler):
    """Inheriting class storing methods do compare movies by runtime."""

    def __init__(self):
        super().__init__('RUNTIME')

    def get_compared_movies_by_runtime(self, first_movie_title, second_movie_title):
        """
        Gets compared movies by runtime.
        :param first_movie_title: <str> -> first script argument (title of the movie)
        :param second_movie_title: <str> -> second script argument (title of the movie)
        :return: <tuple> -> compared movie with higher runtime value
        """
        return self.get_compared_movie_by_value(self.get_movie_by_title(first_movie_title),
                                                self.get_movie_by_title(second_movie_title))


class HighScoreByValueHandler(SortByValueHandler):
    """Inheriting class storing method to get movie high score by value in selected table name."""

    def __init__(self, column):
        super().__init__()
        self.column = column

    def get_movie_high_score_by_value(self):
        """
        Gets movie high score by value in selected table name.
        :return: <tuple> -> title of the movie and high score of value in selected table name
        """
        return self.sort_by_selected_columns([self.column])[0]


class HighScoreByRuntimeHandler(HighScoreByValueHandler):
    """Inheriting class storing methods to get movie with high score in runtime."""

    def __init__(self):
        super().__init__('runtime')

    def get_movie_high_score_by_runtime(self):
        """
        Gets movie with high score in runtime.
        :return: <tuple> -> title of the movie and high score in runtime
        """
        return self.get_movie_high_score_by_value()


class HighScoreByBoxOfficeHandler(HighScoreByValueHandler):
    """Inheriting class storing methods to get movie with high score in box office."""

    def __init__(self):
        super().__init__('box_office')

    def get_movie_high_score_by_box_office(self):
        """
        Gets movie with high score in runtime.
        :return: <tuple> -> title of the movie and high score in box office
        """
        return self.get_movie_high_score_by_value()


class HighScoreByImdbRatingHandler(HighScoreByValueHandler):
    """Inheriting class storing methods to get movie with high score in imdb rating."""

    def __init__(self):
        super().__init__('imdb_rating')

    def get_movie_high_score_by_imdb_rating(self):
        """
        Gets movie with high score in imdb rating.
        :return: <tuple> -> title of the movie and high score in imdb rating
        """
        return self.get_movie_high_score_by_value()


class HighScoreByAwardsWonHandler(QueryHandler):
    """Inheriting class storing methods to get movie with most awards won."""

    def filter_movie_by_most_awards_won(self):
        """
        Filters movies to find the one with most awards won.
        :return: <sqlite3.Row> -> database movie object with most awards won
        """
        return max(self.get_all(), key=lambda movie: AwardsCounter(movie).oscars_wins + AwardsCounter(movie).wins)

    def get_movie_with_most_awards_won(self):
        """
        Gets movie with most awards won.
        :return: <tuple> -> title of the movie and information about awards
        """
        movie = self.filter_movie_by_most_awards_won()
        return movie['title'], movie['awards']


class HighScoreByOscarsWonHandler(QueryHandler):
    """Inheriting class storing methods to get movie with most oscars won."""

    def filter_movie_by_most_oscars_won(self):
        """
        Filters movies to find the one with most oscars won.
        :return: <sqlite3.Row> -> database movie object with most oscars won
        """
        return max(self.get_all(), key=lambda movie: AwardsCounter(movie).oscars_wins)

    def get_movie_with_most_oscars_won(self):
        """
        Gets movie with most oscars won.
        :return: <tuple> -> title of the movie and information about oscars
        """
        movie = self.filter_movie_by_most_oscars_won()
        return movie['title'], movie['awards']


class HighScoreByNominationsHandler(QueryHandler):
    """Inheriting class storing methods to get movie with most nominations."""

    def filter_movie_by_most_nominations(self):
        """
        Filters movies to find the one with most nominations.
        :return: <sqlite3.Row> -> database movie object with most nominations
        """
        return max(self.get_all(), key=lambda movie: AwardsCounter(movie).nominations)

    def get_movie_with_most_nominations(self):
        """
        Gets movie with most nominations.
        :return: <tuple> -> title of the movie and information about awards
        """
        movie = self.filter_movie_by_most_nominations()
        return movie['title'], movie['awards']
