import concurrent.futures

from data_getter import Api


class JsonLoader:
    """Class that loads data stored in json."""

    def __init__(self):
        self.data = []

    def load_movie_from_api(self, movie_title):
        """
        Loads data about movie into object data field.
        :param movie_title: <string> -> title of the movie
        """
        columns = ['Title', 'Year', 'Runtime', 'Genre', 'Director', 'Actors', 'Writer', 'Language', 'Country', 'Awards',
                   'imdbRating', 'imdbVotes', 'BoxOffice']
        movie_data = Api.get(movie_title)
        data = {}
        for column in columns:
            data.update({column: movie_data[column]} if column in movie_data else None)
        self.data.append(data)

    def load_movies_data(self, movie_titles):
        """
        Threading function that loads movies into object data field.
        :param movie_titles: <list> -> list of movie titles
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.load_movie_from_api, movie_titles)
