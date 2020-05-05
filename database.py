import sqlite3
import requests
import concurrent.futures


class Database:

    def __init__(self, name):
        self.name = name
        self.conn = self.open()
        self.cur = self.conn.cursor()

    def __del__(self):
        self.close()

    def open(self):
        db = None
        try:
            db = sqlite3.connect(self.name)
            print('---> Connected to database.')
        except sqlite3.Error:
            print('---> Error connecting to database!')
        return db

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            print('---> Database connection has been closed.')


class Api(Database):

    def __init__(self, name, api_key):
        super().__init__(name)
        self.api_key = api_key
        self.titles = self.get_titles()
        self.data = self.download_movies_data()

    def get_titles(self):
        titles = self.cur.execute('SELECT TITLE FROM MOVIES').fetchall()
        titles = [title for i in titles for title in i]
        return titles

    def get_json_data(self, title):
        columns = ['Year', 'Runtime', 'Genre', 'Director', 'Actors', 'Writer', 'Language', 'Country', 'Awards',
                   'imdbRating', 'imdbVotes', 'BoxOffice', 'Title']
        result = requests.get(f'http://www.omdbapi.com/?t={title}&apikey={self.api_key}').json()
        data = []
        for column in columns:
            data.append(result[column]) if column in result else data.append(None)
        return data

    def download_movies_data(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.get_json_data, self.titles)
        return results

    def update_database(self):
        print('Updating database.')
        for data in self.data:
            query = '''UPDATE MOVIES SET YEAR=?, RUNTIME=?, GENRE=?, DIRECTOR=?, CAST=?, WRITER=?, LANGUAGE=?,
                             COUNTRY=?, AWARDS=?, IMDb_Rating=?, IMDb_votes=?, BOX_OFFICE=? WHERE TRIM(TITLE)=?'''
            self.cur.execute(query, data)
        print('Update complete.')
