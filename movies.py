from database import Database


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
        else:
            query = f'SELECT TITLE, "{self.argument}" FROM MOVIES ORDER BY "{self.argument}" ' \
                f'{self.check_order()}'

        movies = self.cur.execute(query).fetchall()
        for movie in movies:
            print(f'{movie[0]:<50}{movie[1]}')


class FilterBy(Database):

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
            movies = {k: self.wins()[k] for k in self.wins() if k in self.nominations() and int(self.wins()[k]) >
                      int(self.nominations()[k])*0.8}
        elif self.column == 'no_oscars':
            movies = {k: self.nominations_oscars()[k] for k in self.nominations_oscars() if int(self.nominations_oscars()[k]) != 0}
        elif self.column == 'box_office':
            query = f'SELECT TITLE, "{self.column}" FROM MOVIES WHERE CAST(REPLACE(REPLACE("{self.column}" , ' \
                f'",", ""), "$", "") AS DOUBLE) > 100000000'
            movies = dict(self.cur.execute(query).fetchall())
        for key, value in movies.items():
            print(f'{key:<50}{value}')

    def nominations(self):
        awards = self.awards()
        for key, value in awards.items():
            nominations = 0
            if 'Nominated' in value:
                nominations += int(value.split(' ')[2])
            if 'nominations' in value:
                nominations += int(value.split(' ')[-2])
            awards[key] = nominations
        return awards

    def nominations_oscars(self):
        awards = self.awards()
        for key, value in awards.items():
            nominated_oscars = 0
            if 'Nominated' in value and 'Oscar' in value:
                nominated_oscars = int(value.split(' ')[2])
            awards[key] = nominated_oscars
        return awards

    def wins(self):
        awards = self.awards()
        for key, value in awards.items():
            wins = 0
            if 'wins' in value:
                try:
                    win_index = value.split(' ').index('wins')
                    wins = value.split(' ')[win_index - 1]
                except ValueError:
                    pass
            awards[key] = wins
        return awards

    def awards(self):
        query = f'SELECT TITLE, AWARDS FROM MOVIES'
        awards = dict(self.cur.execute(query).fetchall())
        return awards


class CompareBy(Database):

    def __init__(self, name, argument):
        super().__init__(name)
        self.column = argument[0]
        self.first_movie = argument[1]
        self.second_movie = argument[2]

    def compare_by(self):
        query = f'SELECT TITLE, MAX("{self.column}") FROM MOVIES WHERE TITLE LIKE "{self.first_movie}" OR TITLE LIKE ' \
            f'"{self.second_movie}"'
        movies = dict(self.cur.execute(query).fetchall())
        for key, value in movies.items():
            print(f'{key:<50}{value}')
