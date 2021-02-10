import sys
from unittest.mock import patch

import pytest

sys.path.append('./movies')

from data_loader import JsonLoader
from database import DatabaseHandler
from awards_counter import AwardsCounter
from value_formatter import ValueFormatter
from query_handler import QueryHandler, SortByValueHandler, FilterByValueHandler, FilterByNominatedForOscarHandler, \
    FilterByWinsNominationsHandler, FilterByBoxOfficeHandler, CompareByImdbRatingHandler, \
    CompareByBoxOfficeHandler, CompareByAwardsWonHandler, CompareByRuntimeHandler, HighScoreByRuntimeHandler, \
    HighScoreByBoxOfficeHandler, HighScoreByImdbRatingHandler, HighScoreByAwardsWonHandler, \
    HighScoreByOscarsWonHandler, HighScoreByNominationsHandler


@pytest.fixture()
def database_create_table_query():
    return '''CREATE TABLE IF NOT EXISTS MOVIES (
                ID INTEGER primary key,
                TITLE       text,
                YEAR        integer,
                RUNTIME     text,
                GENRE       text,
                DIRECTOR    text,
                CAST        text,
                WRITER      text,
                LANGUAGE    text,
                COUNTRY     text,
                AWARDS      text,
                IMDb_Rating float,
                IMDb_votes  integer,
                BOX_OFFICE  integer
            );'''


@pytest.fixture()
def database_handler_init():
    def __init__(self):
        self.name = ':memory:'
        self.conn = self.open()
        self.cur = self.conn.cursor()

    return __init__


@pytest.fixture()
def database(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_database_handler = DatabaseHandler()
        temp_database_handler.cur.execute(database_create_table_query)
        return temp_database_handler


@pytest.fixture()
def database_with_movie_titles(database):
    database.cur.execute('INSERT INTO MOVIES (TITLE) VALUES ("Interstellar")')
    database.cur.execute('INSERT INTO MOVIES (TITLE) VALUES ("The Godfather")')
    database.cur.execute('INSERT INTO MOVIES (TITLE) VALUES ("Gods")')
    return database


@pytest.fixture()
def movies_data():
    return [{'Title': 'Interstellar', 'Year': '2014', 'Runtime': '169 min', 'Genre': 'Adventure, Drama, Sci-Fi',
             'Director': 'Christopher Nolan',
             'Actors': 'Ellen Burstyn, Matthew McConaughey, Mackenzie Foy, John Lithgow',
             'Writer': 'Jonathan Nolan, Christopher Nolan', 'Language': 'English', 'Country': 'USA, UK, Canada',
             'Awards': 'Won 1 Oscar. Another 43 wins & 148 nominations.', 'imdbRating': '8.6', 'imdbVotes': '1,502,526',
             'BoxOffice': '$188,020,017'},
            {'Title': 'Gods', 'Year': '2008', 'Runtime': '120 min', 'Genre': 'Drama', 'Director': 'Josué Méndez',
             'Actors': 'Maricielo Effio, Sergio Gjurinovic, Anahí de Cárdenas, Edgar Saba',
             'Writer': 'Bárbara Acosta (script), Tito Bonicelli (additional dialogue), Josué Méndez',
             'Language': 'Spanish', 'Country': 'Peru, Argentina, France, Germany', 'Awards': '4 wins & 1 nomination.',
             'imdbRating': '5.8', 'imdbVotes': '300', 'BoxOffice': 'N/A'},
            {'Title': 'The Godfather', 'Year': '1972', 'Runtime': '175 min', 'Genre': 'Crime, Drama',
             'Director': 'Francis Ford Coppola',
             'Actors': 'Marlon Brando, Al Pacino, James Caan, Richard S. Castellano',
             'Writer': 'Mario Puzo (screenplay by), Francis Ford Coppola (screenplay by), Mario Puzo '
                       '(based on the novel by)',
             'Language': 'English, Italian, Latin', 'Country': 'USA',
             'Awards': 'Won 3 Oscars. Another 26 wins & 30 nominations.', 'imdbRating': '9.2', 'imdbVotes': '1,612,983',
             'BoxOffice': '$134,966,411'},
            {'Title': 'Trainspotting', 'Year': '1996', 'Runtime': '93 min', 'Genre': 'Drama', 'Director': 'Danny Boyle',
             'Actors': 'Ewan McGregor, Ewen Bremner, Jonny Lee Miller, Kevin McKidd',
             'Writer': 'Irvine Welsh (based on the novel by), John Hodge (screenplay)', 'Language': 'English',
             'Country': 'UK', 'Awards': 'Nominated for 1 Oscar. Another 23 wins & 34 nominations.', 'imdbRating': '8.1',
             'imdbVotes': '633,057', 'BoxOffice': '$16,491,080'},
            {'Title': 'The Dark Knight Rises', 'Year': '2012', 'Runtime': '164 min', 'Genre': 'Action, Adventure',
             'Director': 'Christopher Nolan', 'Actors': 'Christian Bale, Gary Oldman, Tom Hardy, Joseph Gordon-Levitt',
             'Writer': 'Jonathan Nolan (screenplay), Christopher Nolan (screenplay), Christopher Nolan (story), '
                       'David S. Goyer (story), Bob Kane (characters)',
             'Language': 'English, Arabic', 'Country': 'UK, USA',
             'Awards': 'Nominated for 1 BAFTA Film Award. Another 38 wins & 102 nominations.', 'imdbRating': '8.4',
             'imdbVotes': '1,514,224', 'BoxOffice': '$448,139,099'}

            ]


@pytest.fixture()
def database_with_data(database, movies_data):
    database.insert_movies(movies_data)
    return database


@pytest.fixture()
def movies(database_with_data):
    return database_with_data.cur.execute('SELECT * FROM MOVIES').fetchall()


@pytest.fixture()
def awards_counter_with_interstellar_movie(movies):
    temp_awards_counter = AwardsCounter(movies[0])
    return temp_awards_counter


@pytest.fixture()
def awards_counter_with_trainspotting_movie(movies):
    temp_awards_counter = AwardsCounter(movies[3])
    return temp_awards_counter


@pytest.fixture()
def awards_counter_with_the_dark_knight_rises_movie(movies):
    temp_awards_counter = AwardsCounter(movies[4])
    return temp_awards_counter


@pytest.fixture()
def json_loader():
    temp_json_loader = JsonLoader()
    return temp_json_loader


@pytest.fixture()
def value_formatter():
    temp_value_formatter = ValueFormatter()
    return temp_value_formatter


@pytest.fixture()
def query_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_query_handler = QueryHandler()
        temp_query_handler.cur.execute(database_create_table_query)
        return temp_query_handler


@pytest.fixture()
def query_handler_with_data(query_handler, movies_data):
    query_handler.insert_movies(movies_data)
    return query_handler


@pytest.fixture()
def sort_by_value_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_sort_by_value_handler = SortByValueHandler()
        temp_sort_by_value_handler.cur.execute(database_create_table_query)
        return temp_sort_by_value_handler


@pytest.fixture()
def sort_by_value_handler_with_data(sort_by_value_handler, movies_data):
    sort_by_value_handler.insert_movies(movies_data)
    return sort_by_value_handler


@pytest.fixture()
def filter_by_value_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_filter_by_value_handler = FilterByValueHandler()
        temp_filter_by_value_handler.cur.execute(database_create_table_query)
        return temp_filter_by_value_handler


@pytest.fixture()
def filter_by_value_handler_with_data(filter_by_value_handler, movies_data):
    filter_by_value_handler.insert_movies(movies_data)
    return filter_by_value_handler


@pytest.fixture()
def filter_by_nominated_for_oscar_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_filter_by_nominated_for_oscar_handler = FilterByNominatedForOscarHandler()
        temp_filter_by_nominated_for_oscar_handler.cur.execute(database_create_table_query)
        return temp_filter_by_nominated_for_oscar_handler


@pytest.fixture()
def filter_by_nominated_for_oscar_handler_with_data(filter_by_nominated_for_oscar_handler, movies_data):
    filter_by_nominated_for_oscar_handler.insert_movies(movies_data)
    return filter_by_nominated_for_oscar_handler


@pytest.fixture()
def filter_by_wins_nominations_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_filter_by_wins_nominations_handler = FilterByWinsNominationsHandler()
        temp_filter_by_wins_nominations_handler.cur.execute(database_create_table_query)
        return temp_filter_by_wins_nominations_handler


@pytest.fixture()
def filter_by_wins_nominations_handler_with_data(filter_by_wins_nominations_handler, movies_data):
    filter_by_wins_nominations_handler.insert_movies(movies_data)
    return filter_by_wins_nominations_handler


@pytest.fixture()
def filter_by_box_office_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_filter_by_box_office_handler = FilterByBoxOfficeHandler()
        temp_filter_by_box_office_handler.cur.execute(database_create_table_query)
        return temp_filter_by_box_office_handler


@pytest.fixture()
def filter_by_box_office_handler_with_data(filter_by_box_office_handler, movies_data):
    filter_by_box_office_handler.insert_movies(movies_data)
    return filter_by_box_office_handler


@pytest.fixture()
def compare_by_imdb_rating_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_compare_by_imdb_rating_handler = CompareByImdbRatingHandler()
        temp_compare_by_imdb_rating_handler.cur.execute(database_create_table_query)
        return temp_compare_by_imdb_rating_handler


@pytest.fixture()
def compare_by_imdb_rating_handler_with_data(compare_by_imdb_rating_handler, movies_data):
    compare_by_imdb_rating_handler.insert_movies(movies_data)
    return compare_by_imdb_rating_handler


@pytest.fixture()
def compare_by_box_office_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_compare_by_box_office_handler = CompareByBoxOfficeHandler()
        temp_compare_by_box_office_handler.cur.execute(database_create_table_query)
        return temp_compare_by_box_office_handler


@pytest.fixture()
def compare_by_box_office_handler_with_data(compare_by_box_office_handler, movies_data):
    compare_by_box_office_handler.insert_movies(movies_data)
    return compare_by_box_office_handler


@pytest.fixture()
def compare_by_awards_won_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_compare_by_awards_handler = CompareByAwardsWonHandler()
        temp_compare_by_awards_handler.cur.execute(database_create_table_query)
        return temp_compare_by_awards_handler


@pytest.fixture()
def compare_by_awards_won_handler_with_data(compare_by_awards_won_handler, movies_data):
    compare_by_awards_won_handler.insert_movies(movies_data)
    return compare_by_awards_won_handler


@pytest.fixture()
def compare_by_runtime_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_compare_by_runtime_handler = CompareByRuntimeHandler()
        temp_compare_by_runtime_handler.cur.execute(database_create_table_query)
        return temp_compare_by_runtime_handler


@pytest.fixture()
def compare_by_runtime_handler_with_data(compare_by_runtime_handler, movies_data):
    compare_by_runtime_handler.insert_movies(movies_data)
    return compare_by_runtime_handler


@pytest.fixture()
def high_score_by_runtime_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_high_score_by_runtime_handler = HighScoreByRuntimeHandler()
        temp_high_score_by_runtime_handler.cur.execute(database_create_table_query)
        return temp_high_score_by_runtime_handler


@pytest.fixture()
def high_score_by_runtime_handler_with_data(high_score_by_runtime_handler, movies_data):
    high_score_by_runtime_handler.insert_movies(movies_data)
    return high_score_by_runtime_handler


@pytest.fixture()
def high_score_by_box_office_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_high_score_by_box_office_handler = HighScoreByBoxOfficeHandler()
        temp_high_score_by_box_office_handler.cur.execute(database_create_table_query)
        return temp_high_score_by_box_office_handler


@pytest.fixture()
def high_score_by_box_office_handler_with_data(high_score_by_box_office_handler, movies_data):
    high_score_by_box_office_handler.insert_movies(movies_data)
    return high_score_by_box_office_handler


@pytest.fixture()
def high_score_by_imdb_rating_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_high_score_by_imdb_rating_handler = HighScoreByImdbRatingHandler()
        temp_high_score_by_imdb_rating_handler.cur.execute(database_create_table_query)
        return temp_high_score_by_imdb_rating_handler


@pytest.fixture()
def high_score_by_imdb_rating_handler_with_data(high_score_by_imdb_rating_handler, movies_data):
    high_score_by_imdb_rating_handler.insert_movies(movies_data)
    return high_score_by_imdb_rating_handler


@pytest.fixture()
def high_score_by_awards_won_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_high_score_by_awards_won_handler = HighScoreByAwardsWonHandler()
        temp_high_score_by_awards_won_handler.cur.execute(database_create_table_query)
        return temp_high_score_by_awards_won_handler


@pytest.fixture()
def high_score_by_awards_won_handler_with_data(high_score_by_awards_won_handler, movies_data):
    high_score_by_awards_won_handler.insert_movies(movies_data)
    return high_score_by_awards_won_handler


@pytest.fixture()
def high_score_by_oscars_won_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_high_score_by_oscars_won_handler = HighScoreByOscarsWonHandler()
        temp_high_score_by_oscars_won_handler.cur.execute(database_create_table_query)
        return temp_high_score_by_oscars_won_handler


@pytest.fixture()
def high_score_by_oscars_won_handler_with_data(high_score_by_oscars_won_handler, movies_data):
    high_score_by_oscars_won_handler.insert_movies(movies_data)
    return high_score_by_oscars_won_handler


@pytest.fixture()
def high_score_by_nominations_handler(database_create_table_query, database_handler_init):
    with patch.object(DatabaseHandler, '__init__', database_handler_init):
        temp_high_score_by_nominations_handler = HighScoreByNominationsHandler()
        temp_high_score_by_nominations_handler.cur.execute(database_create_table_query)
        return temp_high_score_by_nominations_handler


@pytest.fixture()
def high_score_by_nominations_handler_with_data(high_score_by_nominations_handler, movies_data):
    high_score_by_nominations_handler.insert_movies(movies_data)
    return high_score_by_nominations_handler
