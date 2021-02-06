import sqlite3


class DatabaseHandler:
    """Class that manages connection to the database, inserts and updates data."""

    def __init__(self):
        self.name = 'movies.sqlite'
        self.conn = self.open()
        self.cur = self.conn.cursor()

    def __del__(self):
        self.close()

    def open(self):
        """
        Opens a connection to the database.
        :return: <sqlite3.Connection> -> database connection
        """
        db = None
        try:
            db = sqlite3.connect(self.name)
            # changing the type of data extracted from the database to the dictionary
            db.row_factory = sqlite3.Row
        except sqlite3.Error:
            print('---> Error connecting to database!')
        return db

    def close(self):
        """Closes a connection to the database."""
        if self.conn:
            self.conn.commit()
            self.cur.close()
            self.conn.close()

    def update_movie_data(self, movie):
        """
        Updates single movie data in the database.
        :param movie: <string> -> title of the movie
        """
        query = '''UPDATE MOVIES SET YEAR=:Year, RUNTIME=:Runtime, GENRE=:Genre, DIRECTOR=:Director, CAST=:Actors, 
        WRITER=:Writer, LANGUAGE=:Language, COUNTRY=:Country, AWARDS=:Awards, IMDb_Rating=:imdbRating, 
        IMDb_votes=:imdbVotes, BOX_OFFICE=:BoxOffice WHERE TRIM(TITLE)=:Title'''
        self.cur.execute(query, movie)

    def update_movies(self, movies):
        """
        Updates movies data in the database.
        :param movies: <list> -> list of movie titles
        """
        for movie in movies:
            self.update_movie_data(movie)

    def insert_movie_data(self, movie):
        """
        Inserts single movie data in the database.
        :param movie: <string> -> title of the movie
        """
        query = '''INSERT INTO MOVIES (TITLE, YEAR, RUNTIME, GENRE, DIRECTOR, CAST, WRITER, LANGUAGE, COUNTRY, 
        AWARDS, IMDb_Rating, IMDb_votes, BOX_OFFICE) VALUES (:Title, :Year, :Runtime, :Genre, :Director, :Actors, 
        :Writer, :Language, :Country, :Awards, :imdbRating, :imdbVotes, :BoxOffice)'''
        self.cur.execute(query, movie)

    def insert_movies(self, movies):
        """
        Inserts movies data in the database.
        :param movies: <list> -> list of movie titles
        """
        for movie in movies:
            self.insert_movie_data(movie)
