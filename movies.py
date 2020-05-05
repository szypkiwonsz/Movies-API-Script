from database import Database


class SortBy(Database):

    def __init__(self, name, argument):
        super().__init__(name)
        self.argument = argument

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
        self.column = argument[0]
        self.parameter = argument[1]

    def filter_by(self):
        query = f'SELECT TITLE, "{self.column}" FROM MOVIES WHERE "{self.column}" LIKE "%{self.parameter}%"'
        movies = self.cur.execute(query).fetchall()
        for movie in movies:
            print(f'{movie[0]:<50}{movie[1]}')
