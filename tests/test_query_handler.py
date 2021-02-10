import pytest


@pytest.mark.query
def test_get_all(query_handler_with_data):
    assert query_handler_with_data.get_all()[0]['title'] == 'Interstellar'
    assert query_handler_with_data.get_all()[1]['title'] == 'Gods'


@pytest.mark.query
def test_get_all_titles(query_handler_with_data):
    assert query_handler_with_data.get_all_titles()[0] == 'Interstellar'


@pytest.mark.query
def test_sort_movies_data_by_columns_decreasing(sort_by_value_handler_with_data):
    list_of_movies = sort_by_value_handler_with_data.cur.execute('SELECT * FROM MOVIES').fetchall()
    sorted_movies = sort_by_value_handler_with_data.sort_movies_data_by_columns_decreasing(list_of_movies, ['year'])
    assert sorted_movies[0]['year'] == 2014
    assert sorted_movies[1]['year'] == 2012


@pytest.mark.query
def test_get_data_to_sort(sort_by_value_handler_with_data):
    assert sort_by_value_handler_with_data.get_data_to_sort()[0]['title'] == 'Interstellar'


@pytest.mark.query
def test_sort_by_selected_columns(sort_by_value_handler_with_data):
    assert sort_by_value_handler_with_data.sort_by_selected_columns(['imdb_rating'])[0] == ('The Godfather', 9.2)
    assert sort_by_value_handler_with_data.sort_by_selected_columns(['imdb_rating'])[1] == ('Interstellar', 8.6)


@pytest.mark.query
def test_get_filtered_movies_by_value(filter_by_value_handler_with_data):
    assert filter_by_value_handler_with_data.get_filtered_movies_by_value('director', 'nolan')[0] == (
        'Interstellar', 'Christopher Nolan')
    assert filter_by_value_handler_with_data.get_filtered_movies_by_value('cast', 'matthew')[0] == (
        'Interstellar', 'Ellen Burstyn, Matthew McConaughey, Mackenzie Foy, John Lithgow')


@pytest.mark.query
def test_filter_movies_by_value(filter_by_value_handler_with_data):
    filter_by_value_handler_with_data.filter_movies_by_value('director', 'nolan')
    assert filter_by_value_handler_with_data.filtered_movies[0]['title'] == 'Interstellar'
    assert filter_by_value_handler_with_data.filtered_movies[0]['director'] == 'Christopher Nolan'


@pytest.mark.query
def test_get_filtered_movies_by_nomination_for_oscar(filter_by_nominated_for_oscar_handler_with_data):
    assert filter_by_nominated_for_oscar_handler_with_data.get_filtered_movies_by_nomination_for_oscar()[0] == (
        'Trainspotting', 'Nominated for 1 Oscar. Another 23 wins & 34 nominations.')


@pytest.mark.query
def test_check_nomination_for_oscar(
        filter_by_nominated_for_oscar_handler_with_data, awards_counter_with_trainspotting_movie):
    filter_by_nominated_for_oscar_handler_with_data.check_nomination_for_oscar(awards_counter_with_trainspotting_movie)
    assert filter_by_nominated_for_oscar_handler_with_data.filtered_movies[0] == (
        'Trainspotting', 'Nominated for 1 Oscar. Another 23 wins & 34 nominations.')


@pytest.mark.query
def test_filter_movies_by_nomination_for_oscar(filter_by_nominated_for_oscar_handler_with_data):
    filter_by_nominated_for_oscar_handler_with_data.filter_movies_by_nomination_for_oscar()
    assert filter_by_nominated_for_oscar_handler_with_data.filtered_movies[0] == (
        'Trainspotting', 'Nominated for 1 Oscar. Another 23 wins & 34 nominations.')


@pytest.mark.query
def test_get_filtered_movies_by_wins_nominations(filter_by_wins_nominations_handler_with_data):
    filter_by_wins_nominations_handler_with_data.get_filtered_movies_by_wins_nominations()
    assert filter_by_wins_nominations_handler_with_data.filtered_movies[0] == ('Gods', '4 wins & 1 nomination.')


@pytest.mark.query
def test_check_wins_nominations(
        filter_by_wins_nominations_handler_with_data, awards_counter_with_trainspotting_movie):
    filter_by_wins_nominations_handler_with_data.check_wins_nominations(awards_counter_with_trainspotting_movie)
    assert filter_by_wins_nominations_handler_with_data.filtered_movies == []


@pytest.mark.query
def test_filter_movies_by_wins_nominations(filter_by_wins_nominations_handler_with_data):
    filter_by_wins_nominations_handler_with_data.filter_movies_by_wins_nominations()
    assert filter_by_wins_nominations_handler_with_data.filtered_movies[0] == ('Gods', '4 wins & 1 nomination.')


@pytest.mark.query
def test_get_filtered_movies_by_box_office(filter_by_box_office_handler_with_data):
    assert filter_by_box_office_handler_with_data.get_filtered_movies_by_box_office()[0] == (
        'Interstellar', '$188,020,017')


@pytest.mark.query
def test_filter_movies_by_box_office(filter_by_box_office_handler_with_data):
    filter_by_box_office_handler_with_data.filter_movies_by_box_office()
    assert filter_by_box_office_handler_with_data.filtered_movies[0]['title'] == 'Interstellar'


@pytest.mark.query
def test_get_compared_movies_by_imdb_rating(compare_by_imdb_rating_handler_with_data):
    assert compare_by_imdb_rating_handler_with_data.get_compared_movies_by_imdb_rating('Interstellar', 'Gods') == (
        'Interstellar', 8.6)


@pytest.mark.query
def test_get_compared_movies_by_box_office(compare_by_box_office_handler_with_data):
    assert compare_by_box_office_handler_with_data.get_compared_movies_by_box_office('Interstellar', 'Gods') == (
        'Interstellar', '$188,020,017')


@pytest.mark.query
def test_get_compared_movies_by_awards_won(compare_by_awards_won_handler_with_data):
    assert compare_by_awards_won_handler_with_data.get_compared_movies_by_awards_won('Interstellar', 'Gods') == (
        'Interstellar', 'Won 1 Oscar. Another 43 wins & 148 nominations.')


@pytest.mark.query
def test_get_compared_movies_by_runtime(compare_by_runtime_handler_with_data):
    assert compare_by_runtime_handler_with_data.get_compared_movies_by_runtime('Interstellar', 'Gods') == (
        'Interstellar', '169 min')


@pytest.mark.query
def test_get_movie_high_score_by_runtime(high_score_by_runtime_handler_with_data):
    assert high_score_by_runtime_handler_with_data.get_movie_high_score_by_runtime() == ('The Godfather', '175 min')


@pytest.mark.query
def test_get_movie_high_score_by_imdb_rating(high_score_by_imdb_rating_handler_with_data):
    assert high_score_by_imdb_rating_handler_with_data.get_movie_high_score_by_imdb_rating() == ('The Godfather', 9.2)


@pytest.mark.query
def test_get_movie_high_score_by_box_office(high_score_by_box_office_handler_with_data):
    assert high_score_by_box_office_handler_with_data.get_movie_high_score_by_box_office() == (
        'The Dark Knight Rises', '$448,139,099')


@pytest.mark.query
def test_filter_movie_by_most_awards_won(high_score_by_awards_won_handler_with_data):
    assert high_score_by_awards_won_handler_with_data.filter_movie_by_most_awards_won()['title'] == 'Interstellar'


@pytest.mark.query
def test_get_movie_with_most_awards_won(high_score_by_awards_won_handler_with_data):
    assert high_score_by_awards_won_handler_with_data.get_movie_with_most_awards_won() == (
        'Interstellar', 'Won 1 Oscar. Another 43 wins & 148 nominations.')


@pytest.mark.query
def test_filter_movie_by_most_oscars_won(high_score_by_oscars_won_handler_with_data):
    assert high_score_by_oscars_won_handler_with_data.filter_movie_by_most_oscars_won()['title'] == 'The Godfather'


@pytest.mark.query
def test_get_movie_with_most_oscars_won(high_score_by_oscars_won_handler_with_data):
    assert high_score_by_oscars_won_handler_with_data.get_movie_with_most_oscars_won() == (
        'The Godfather', 'Won 3 Oscars. Another 26 wins & 30 nominations.')


@pytest.mark.query
def test_filter_movie_by_most_nominations(high_score_by_nominations_handler_with_data):
    assert high_score_by_nominations_handler_with_data.filter_movie_by_most_nominations()['title'] == 'Interstellar'


@pytest.mark.query
def test_get_movie_with_most_nominations(high_score_by_nominations_handler_with_data):
    assert high_score_by_nominations_handler_with_data.get_movie_with_most_nominations() == (
        'Interstellar', 'Won 1 Oscar. Another 43 wins & 148 nominations.')
