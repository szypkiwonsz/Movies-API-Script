import pytest


@pytest.mark.value_formatter
def test_is_award_value_true(value_formatter):
    assert value_formatter.is_award_value('Nominated for 1 BAFTA Film Award. Another 38 wins & 102 nominations.')


@pytest.mark.value_formatter
def test_is_award_value_false(value_formatter):
    assert not value_formatter.is_award_value('$448,139,099')


@pytest.mark.value_formatter
def test_is_float_value_true(value_formatter):
    assert value_formatter.is_float_value(1.0)


@pytest.mark.value_formatter
def test_has_digit_false(value_formatter):
    assert not value_formatter.is_float_value('$448,139,099')


@pytest.mark.value_formatter
def test_prepare_value_award_value(value_formatter):
    assert value_formatter.prepare_value('Won 2 Oscars. Another 19 wins & 32 nominations.') == 53


@pytest.mark.value_formatter
def test_prepare_value_imdb_rating_value(value_formatter):
    assert value_formatter.prepare_value(2.0) == 2.0


@pytest.mark.value_formatter
def test_prepare_value_box_office_value(value_formatter):
    assert value_formatter.prepare_value('$448,139,099') == 448139099


@pytest.mark.value_formatter
def test_prepare_value_runtime_value(value_formatter):
    assert value_formatter.prepare_value('120 min') == 120


@pytest.mark.value_formatter
def test_prepare_value_imdb_votes_value(value_formatter):
    assert value_formatter.prepare_value('600,000') == 600000


@pytest.mark.value_formatter
def test_prepare_value_year_value(value_formatter):
    assert value_formatter.prepare_value('2020') == 2020


@pytest.mark.value_formatter
def test_prepare_value_string_value(value_formatter):
    assert value_formatter.prepare_value('Interstellar') == 'Interstellar'
