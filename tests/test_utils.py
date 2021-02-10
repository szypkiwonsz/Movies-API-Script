import pytest

from utils import change_string_with_numbers_to_int


@pytest.mark.utils
def test_change_string_with_numbers_to_int():
    assert change_string_with_numbers_to_int('$404,202,554') == 404202554
