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


class SortByValuesHandler(QueryHandler, ValueFormatter):
    """Class storing methods for sorting data about movies from database."""

    def sort_movies_data_by_table_names_decreasing(self, list_of_movies, table_names):
        """
        Sorts list of tuples without the first one tuple which is title of the movie.
        :param list_of_movies: <list> -> list of database objects - movies
        :param table_names: <tuple> -> argument(s) from script
        :return: <list> -> sorted list of database objects - movies
        """
        return sorted(list_of_movies, key=lambda x: [
            self.prepare_value(str(x[table_name]) if x[table_name] != 'N/A' else str(0)) for table_name in
            table_names], reverse=True)

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


class CompareByValue(QueryHandler, ValueFormatter):
    """Inheriting class storing methods for comparing two movies by selected value."""

    def __init__(self, table_name):
        super().__init__()
        self.table_name = table_name

    def compare_movies_by_value(self, first_movie, second_movie):
        """
        Compares two movies by value.
        :param first_movie: <sqlite3.Row> -> database object of first movie to compare
        :param second_movie: <sqlite3.Row> -> database object of second movie to compare
        :return: <sqlite3.Row> -> database movie object with higher compared value
        """
        return max([first_movie, second_movie], key=lambda x: self.prepare_value(x[self.table_name]))

    def get_compared_movie_by_value(self, first_movie, second_movie):
        """Gets compared movie by higher value.
        :param first_movie: <sqlite3.Row> -> database object of first movie to compare
        :param second_movie: <sqlite3.Row> -> database object of second movie to compare
        :return: <tuple> -> compared movie with higher value
        """
        movie = self.compare_movies_by_value(first_movie, second_movie)
        return movie['title'], movie[self.table_name]

    def get_movie_by_title(self, movie_title):
        """
        Gets movie database object by title.
        :param movie_title: <str> -> title of the movie
        :return: <str> -> movie database object
        """
        return [x for x in self.get_all() if x['title'] == movie_title][0]


class CompareByImdbRating(CompareByValue):
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


class CompareByBoxOffice(CompareByValue):
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


class CompareByAwardsWon(CompareByValue):
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


class CompareByRuntime(CompareByValue):
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
