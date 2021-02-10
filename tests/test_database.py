import pytest


@pytest.mark.database
def test_update_movie_data(database_with_movie_titles, movies_data):
    database_with_movie_titles.update_movie_data(movies_data[0])
    movies = database_with_movie_titles.cur.execute(f'SELECT * FROM MOVIES').fetchall()
    assert movies[0]['year'] == 2014


@pytest.mark.database
def test_update_movies(database_with_movie_titles, movies_data):
    database_with_movie_titles.update_movies(movies_data)
    movies = database_with_movie_titles.cur.execute(f'SELECT * FROM MOVIES').fetchall()
    assert movies[1]['year'] == 1972


@pytest.mark.database
def test_insert_movie_data(database, movies_data):
    database.insert_movie_data(movies_data[0])
    movies = database.cur.execute(f'SELECT * FROM MOVIES').fetchall()
    assert movies[0]['title'] == 'Interstellar'


@pytest.mark.database
def test_insert_movies(database, movies_data):
    database.insert_movies(movies_data)
    movies = database.cur.execute(f'SELECT * FROM MOVIES').fetchall()
    assert movies[1]['title'] == 'Gods'
