import pytest


@pytest.mark.awards_counter
def test_scrape_awards_interstellar(awards_counter_with_interstellar_movie):
    """This function is performed when the object is initialized and also tests 'scrape_oscar_wins',
    'scrape_oscar_nominations', 'scrape_wins', 'scrape_nominations'."""
    assert awards_counter_with_interstellar_movie.oscars_wins == 1
    assert awards_counter_with_interstellar_movie.oscars_nominations == 0
    assert awards_counter_with_interstellar_movie.nominations == 148
    assert awards_counter_with_interstellar_movie.wins == 43


@pytest.mark.awards_counter
def test_scrape_awards_trainspotting(awards_counter_with_trainspotting_movie):
    """This function is performed when the object is initialized and also tests 'scrape_oscar_wins',
    'scrape_oscar_nominations', 'scrape_wins', 'scrape_nominations'."""
    assert awards_counter_with_trainspotting_movie.oscars_wins == 0
    assert awards_counter_with_trainspotting_movie.oscars_nominations == 1
    assert awards_counter_with_trainspotting_movie.nominations == 34
    assert awards_counter_with_trainspotting_movie.wins == 23


@pytest.mark.awards_counter
def test_scrape_awards_the_dark_knight_rises(awards_counter_with_the_dark_knight_rises_movie):
    """This function is performed when the object is initialized and also tests 'scrape_oscar_wins',
    'scrape_oscar_nominations', 'scrape_wins', 'scrape_nominations'."""
    assert awards_counter_with_the_dark_knight_rises_movie.oscars_wins == 0
    assert awards_counter_with_the_dark_knight_rises_movie.oscars_nominations == 0
    assert awards_counter_with_the_dark_knight_rises_movie.nominations == 102
    assert awards_counter_with_the_dark_knight_rises_movie.wins == 38
