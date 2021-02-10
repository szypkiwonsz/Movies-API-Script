import pytest
from requests import HTTPError

from data_getter import Api


@pytest.mark.api
def test_get_200(requests_mock):
    requests_mock.get('http://www.omdbapi.com/?t=Interstellar&apikey=39f41e43',
                      json={'name': 'awesome-mock', 'Response': 'True'})
    response = Api.get('http://www.omdbapi.com/?t=Interstellar&apikey=39f41e43')
    assert response['name'] == 'awesome-mock'


@pytest.mark.api
def test_get_404(requests_mock):
    requests_mock.get('http://www.omdbapi.com/?t=Interstellar&apikey=39f41e43', status_code=404)
    with pytest.raises(HTTPError):
        response = Api.get('http://www.omdbapi.com/?t=Interstellar&apikey=39f41e43')


@pytest.mark.api
def test_get_response_false(requests_mock):
    requests_mock.get('http://www.omdbapi.com/?t=Interstellar&apikey=39f41e43', json={'Response': 'False'})
    with pytest.raises(HTTPError):
        response = Api.get('http://www.omdbapi.com/?t=Interstellar&apikey=39f41e43')
