import pytest
from projects.utils import utils


def test__query_params_can_be_built() -> None:
    params = {
        "key1": 1,
        "key2": "thingy",
        "key3": None,
        "key4": "",
        "key5": 0,
        "key6": False,
    }
    result = utils.to_param_string(params)

    assert result == "?key1=1&key2=thingy&key4=&key5=0&key6=False"


@pytest.mark.parametrize("params", [None, {}])
def test__empty_query_params_return_an_empty_string(params: dict) -> None:
    assert utils.to_param_string(params) == ""


def test__all_query_params_can_be_kept() -> None:
    params = {
        "key1": None,
        "key2": "",
        "key3": 0,
        "key4": False,
    }
    result = utils.to_param_string(params, keep_all=True)

    assert result == "?key1=&key2=&key3=0&key4=False"
