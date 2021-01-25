import requests


class Api:
    """Class storing method to get data from api."""

    @staticmethod
    def get(movie_title):
        """
        Gets data about movie by title.
        :param movie_title: <string> -> title of the movie
        :return: <dict> -> json data from api
        """
        response = requests.get(f'http://www.omdbapi.com/?t={movie_title}&apikey=39f41e43')
        if response.status_code != 200:
            raise requests.HTTPError(f'{response.status_code}')
        else:
            return response.json()
