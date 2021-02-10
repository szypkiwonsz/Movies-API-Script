import requests


class Api:
    """Class storing method to get data from api."""

    @staticmethod
    def get(url):
        """
        Gets data about movie by title.
        :param url: <string> -> api url
        :return: <dict> -> json data from api
        """
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.HTTPError(f'{response.status_code}')
        elif response.json()['Response'] == 'False':
            # raises 204 response status code if there is no data about movie
            raise requests.HTTPError(204)
        else:
            return response.json()
