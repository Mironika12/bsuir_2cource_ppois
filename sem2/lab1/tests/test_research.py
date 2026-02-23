import pytest
from domain.research import Research


def test_add_reference_success():
    r = Research()
    r.add_reference({"reference": "ГОСТ"})

    assert len(r.references) == 1
    assert r.references[0]["is_read"] is False


def test_mark_as_read():
    r = Research()
    r.add_reference({"reference": "ГОСТ"})
    r.mark_as_read(0)

    assert r.references[0]["is_read"] is True


def test_invalid_reference():
    r = Research()

    with pytest.raises(ValueError):
        r.add_reference({"wrong": "data"})