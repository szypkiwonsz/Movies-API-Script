import sqlite3
import requests


class Database:

    # Opens database connection.
    def __init__(self, name, table):

        try:
            self.connect = sqlite3.connect(name)
            self.cursor = self.connect.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")

        self.table = table

    # Closes database connection.
    def close(self):

        if self.connect:
            self.connect.commit()
            self.cursor.close()
            self.connect.close()

    # Gets data from database by table and column name.
    def select(self, column):

        query = "SELECT {} FROM {}".format(column, self.table)
        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        return rows

    # Updates database column with values.
    def update(self, table, column, update, where_column, value):
        self.cursor.execute("UPDATE {} SET {} = ? WHERE {} = ?".format(table, column, where_column),
                            (update, value))

    def insert(self, title, year=None, runtime=None, genre=None, director=None, cast=None, writer=None,
               language=None, country=None, awards=None, imdb_rating=None, imdb_votes=None, box_office=None):
        self.cursor.execute("INSERT INTO MOVIES (TITLE, YEAR, RUNTIME, GENRE, DIRECTOR, CAST, WRITER, LANGUAGE, "
                            "COUNTRY, AWARDS, IMDb_Rating, IMDb_votes, BOX_OFFICE) VALUES "
                            "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (title, year, runtime, genre,
                                                                        director, cast, writer, language,
                                                                        country, awards, imdb_rating,
                                                                        imdb_votes, box_office))

    # Gets data from api and inserts into database.
    def get_data(self):

        titles = Database.select(self, "TITLE")
        print("Getting data from api:")

        for movie in range(len(titles)):
            print("Getting {} movie data...".format(",".join(titles[movie])))
            results = (requests.get('http://www.omdbapi.com/?t=' + ",".join(titles[movie]) + '&apikey=39f41e43'))
            # Inserting results of api data into dictionary.
            results = eval(results.text)

            # Checking if data for movie exist and if not set value as null.
            if results.get("Year"):
                Database.update(self, "MOVIES", "YEAR", results["Year"], "ID", movie)
            else:
                continue
            if results.get("Runtime"):
                Database.update(self, "MOVIES", "RUNTIME", results["Runtime"], "ID", movie)
            else:
                continue
            if results.get("Genre"):
                Database.update(self, "MOVIES", "GENRE", results["Genre"], "ID", movie)
            else:
                continue
            if results.get("Director"):
                Database.update(self, "MOVIES", "DIRECTOR", results["Director"], "ID", movie)
            else:
                continue
            if results.get("Actors"):
                Database.update(self, "MOVIES", "CAST", results["Actors"], "ID", movie)
            else:
                continue
            if results.get("Writer"):
                Database.update(self, "MOVIES", "WRITER", results["Writer"], "ID", movie)
            else:
                continue
            if results.get("Language"):
                Database.update(self, "MOVIES", "LANGUAGE", results["Language"], "ID", movie)
            else:
                continue
            if results.get("Country"):
                Database.update(self, "MOVIES", "COUNTRY", results["Country"], "ID", movie)
            else:
                continue
            if results.get("Awards"):
                Database.update(self, "MOVIES", "AWARDS", results["Awards"], "ID", movie)
            else:
                continue
            if results.get("imdbRating"):
                Database.update(self, "MOVIES", "IMDb_Rating", results["imdbRating"], "ID", movie)
            else:
                continue
            if results.get("imdbVotes"):
                Database.update(self, "MOVIES", "IMDb_votes", results["imdbVotes"], "ID", movie)
            else:
                continue
            if results.get("BoxOffice"):
                Database.update(self, "MOVIES", "BOX_OFFICE", results["BoxOffice"], "ID", movie)
            else:
                continue
        print("Finished getting and updating database with api data.")
