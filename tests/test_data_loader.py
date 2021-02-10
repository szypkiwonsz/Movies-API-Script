import pytest


@pytest.mark.json_loader
def test_load_movie_from_api(json_loader, movies_data):
    json_loader.load_movie_from_api('Interstellar')
    assert json_loader.data[0] == movies_data[0]


@pytest.mark.json_loader
def test_load_movies_data(json_loader, movies_data):
    json_loader.load_movies_data(['Interstellar'])
    assert json_loader.data[0] == movies_data[0]
