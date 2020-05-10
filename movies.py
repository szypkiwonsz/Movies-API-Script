import sqlite3
import sys

from database import Database, Api


class Functions:

    @staticmethod
    def box_office_characters(movies):
        for key, value in movies.items():
            movies[key] = '${:,}'.format(value)
        return movies

    @staticmethod
    def runtime_character(movies):
        for key, value in movies.items():
            hours = value // 60
            minutes = value % 60
            movies[key] = f'{hours}h {minutes}min'
        return movies

    @staticmethod
    def wins(awards):
        for key, value in awards.items():
            wins = 0
            try:
                if 'wins' in value:
                    try:
                        win_index = value.split(' ').index('wins')
                        wins = value.split(' ')[win_index - 1]
                    except ValueError:
                        wins = 0
            except TypeError:
                wins = 0
            awards[key] = wins
        return awards

    @staticmethod
    def nominations(awards):
        for key, value in awards.items():
            nominations = 0
            try:
                if 'Nominated' in value:
                    nominations += int(value.split(' ')[2])
                if 'nominations' in value:
                    nominations += int(value.split(' ')[-2])
            except TypeError:
                nominations += 0
            awards[key] = nominations
        return awards

    @staticmethod
    def oscars(awards):
        for key, value in awards.items():
            nominated_oscars = 0
            try:
                if 'Won' in value and 'Oscar' in value:
                    nominated_oscars = int(value.split(' ')[1])
            except TypeError:
                nominated_oscars = 0
            awards[key] = nominated_oscars
        return awards


class SortBy(Database):

    def __init__(self, name, argument):
        super().__init__(name)
        self.argument = argument.lower()

    def check_order(self):
        sort_desc = ['year', 'runtime', 'imdb_rating', 'imdb_votes', 'box_office']
        if self.argument in sort_desc:
            order = 'DESC'
        else:
            order = 'ASC'
        return order

    def sort_by(self):
        column_cast = ['runtime', 'year']
        column_imdb_votes = ['imdb_votes']
        column_box_office = ['box_office']
        if self.argument in column_cast:
            query = f'SELECT TITLE, "{self.argument}" FROM MOVIES ORDER BY CAST("{self.argument}" AS DOUBLE) ' \
                f'{self.check_order()}'
        elif self.argument in column_imdb_votes:
            query = f'SELECT TITLE, "{self.argument}" FROM MOVIES ORDER BY CAST(REPLACE("{self.argument}" , ",", "") ' \
                f'AS DOUBLE) {self.check_order()}'
        elif self.argument in column_box_office:
            query = f'SELECT TITLE, "{self.argument}" FROM MOVIES ORDER BY CAST(REPLACE(REPLACE("{self.argument}" , ' \
                f'",", ""), "$", "") AS DOUBLE) {self.check_order()}'
        elif self.argument.isalpha():
            query = f'SELECT TITLE, {self.argument} FROM MOVIES ORDER BY "{self.argument}" ' \
                f'{self.check_order()}'
        else:
            sys.exit(f'Database column does not exist: {self.argument}')
        try:
            movies = self.cur.execute(query).fetchall()
        except sqlite3.OperationalError:
            sys.exit(f'Database column does not exist: {self.argument}')
        for movie in movies:
            print(f'{movie[0]:<50}{movie[1]}')


class FilterBy(Database, Functions):

    def __init__(self, name, argument):
        super().__init__(name)
        self.column = argument[0].lower()
        self.parameter = self.get_parameter(argument)

    def get_parameter(self, argument):
        try:
            self.parameter = argument[1].lower()
        except IndexError:
            self.parameter = None
        return self.parameter

    def filter_by(self):
        movies = {}
        column = ['director', 'cast', 'language']
        if self.column in column:
            query = f'SELECT TITLE, "{self.column}" FROM MOVIES WHERE "{self.column}" LIKE "%{self.parameter}%"'
            movies = dict(self.cur.execute(query).fetchall())
        elif self.column == 'awards':
            movies = {k: self.wins(self.awards())[k] for k in self.wins(self.awards()) if
                      k in self.nominations(self.awards()) and int(self.wins(self.awards())[k]) >
                      int(self.nominations(self.awards())[k]) * 0.8}
        elif self.column == 'no_oscars':
            movies = {k: self.nominations_oscars()[k] for k in self.nominations_oscars() if
                      int(self.nominations_oscars()[k]) != 0}
        elif self.column == 'box_office':
            query = f'SELECT TITLE, "{self.column}" FROM MOVIES WHERE CAST(REPLACE(REPLACE("{self.column}" , ' \
                f'",", ""), "$", "") AS DOUBLE) > 100000000'
            movies = dict(self.cur.execute(query).fetchall())
        if movies.items():
            for key, value in movies.items():
                print(f'{key:<50}{value}')
        else:
            sys.exit('No data.')

    def nominations_oscars(self):
        awards = self.awards()
        for key, value in awards.items():
            nominated_oscars = 0
            try:
                if 'Nominated' in value and 'Oscar' in value:
                    nominated_oscars = int(value.split(' ')[2])
            except TypeError:
                nominated_oscars = 0
            awards[key] = nominated_oscars
        return awards

    def awards(self):
        query = f'SELECT TITLE, AWARDS FROM MOVIES'
        awards = dict(self.cur.execute(query).fetchall())
        return awards


class CompareBy(Database, Functions):

    def __init__(self, name, argument):
        super().__init__(name)
        self.column = argument[0]
        self.first_movie = argument[1]
        self.second_movie = argument[2]

    def compare_by(self):
        if self.column == 'imdb_rating':
            query = f'SELECT TITLE, MAX(CAST("{self.column}"AS DOUBLE)) FROM MOVIES WHERE TITLE LIKE ' \
                f'"{self.first_movie}" OR TITLE LIKE "{self.second_movie}"'
            movies = dict(self.cur.execute(query).fetchall())
        elif self.column == 'box_office':
            query = f'SELECT TITLE, MAX(CAST(REPLACE(REPLACE("{self.column}" , ",", ""), "$", "") AS DOBULE)) FROM ' \
                f'MOVIES WHERE TITLE LIKE "{self.first_movie}" OR TITLE LIKE "{self.second_movie}"'
            movies = dict(self.cur.execute(query).fetchall())
            movies = self.box_office_characters(movies)
        elif self.column == 'runtime':
            query = f'SELECT TITLE, MAX(CAST("{self.column}"AS INTEGER)) FROM MOVIES WHERE TITLE LIKE ' \
                f'"{self.first_movie}" OR TITLE LIKE "{self.second_movie}"'
            movies = dict(self.cur.execute(query).fetchall())
            movies = self.runtime_character(movies)
        else:
            query = f'SELECT TITLE, AWARDS FROM MOVIES WHERE TITLE LIKE ' \
                f'"{self.first_movie}" OR TITLE LIKE "{self.second_movie}"'
            movies = dict(self.cur.execute(query).fetchall())
            movies = self.wins(movies)
            try:
                movies = max(movies.items(), key=lambda k: k[1])
                movies = dict([movies])
            except ValueError:
                sys.exit('Incorrect movie titles or no data.')

        for key, value in movies.items():
            print(f'{key:<50}{value}')


class AddMovie(Api):

    def __init__(self, name, api_key, title):
        super().__init__(name, api_key)
        self.title = title

    def add_movie(self):
        query = f'SELECT TITLE FROM MOVIES WHERE TITLE = "{self.title}"'
        is_movie = list(self.cur.execute(query))
        if is_movie:
            print('This movie already exist in database.')
        else:
            query = f'INSERT INTO MOVIES (TITLE) VALUES ("{self.title}")'
            self.cur.execute(query)


class Highscores(Database, Functions):

    def __init__(self, name):
        super().__init__(name)
        self.highscore_runtime = self.runtime()
        self.highscore_box_office = self.box_office()
        self.highscore_awards = self.awards(self.wins)
        self.highscore_nominations = self.awards(self.nominations)
        self.highscore_oscars = self.awards(self.oscars)
        self.highscore_imdb_rating = self.imdb_rating()

    def runtime(self):
        query_runtime = f'SELECT TITLE, MAX(CAST(RUNTIME AS INTEGER)) FROM MOVIES'
        highscore_runtime = dict(self.cur.execute(query_runtime))
        highscore_runtime = self.runtime_character(highscore_runtime)
        return highscore_runtime

    def box_office(self):
        query_boxoffice = f'SELECT TITLE, MAX(CAST(REPLACE(REPLACE(BOX_OFFICE , ",", ""), "$", "") AS DOBULE)) ' \
            f'FROM MOVIES'
        highscore_box_office = dict(self.cur.execute(query_boxoffice))
        highscore_box_office = self.box_office_characters(highscore_box_office)
        return highscore_box_office

    def awards(self, function):
        query_awards = f'SELECT TITLE, AWARDS FROM MOVIES'
        highscore_awards = dict(self.cur.execute(query_awards))
        highscore_awards = function(highscore_awards)
        highscore_awards = max(highscore_awards.items(), key=lambda k: int(k[1]))
        highscore_awards = dict([highscore_awards])
        return highscore_awards

    def imdb_rating(self):
        query_imdb_rating = f'SELECT TITLE, MAX(CAST(IMDB_RATING AS DOUBLE)) FROM MOVIES'
        highscore_imdb_rating = dict(self.cur.execute(query_imdb_rating))
        return highscore_imdb_rating

    @staticmethod
    def print(dictionary, column):
        for key, value in dictionary.items():
            print(f'{column:<50}{key:<50}{value}')

    def highscores(self):
        self.print(self.highscore_runtime, 'Runtime')
        self.print(self.highscore_box_office, 'Box Office')
        self.print(self.highscore_awards, 'Awards')
        self.print(self.highscore_nominations, 'Nominations')
        self.print(self.highscore_oscars, 'Oscars')
        self.print(self.highscore_imdb_rating, 'Runtime')
