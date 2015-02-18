import pytest


class DummyTable(object):
    __table_name__ = "dummy_table_name"


class DummyTableNotFound(object):
    pass


@pytest.mark.parametrize("obj, expected", [
    ("dummy_table_name", "dummy_table_name"),
    (DummyTable, "dummy_table_name"),
])
def test_table_from_obj(obj, expected):
    from api.database import _table_name_from_obj
    assert _table_name_from_obj(obj) == expected


def test_table_from_unsupported_obj():
    from api.database import _table_name_from_obj

    with pytest.raises(AssertionError):
        obj = DummyTableNotFound()
        assert _table_name_from_obj(obj) == "a_table"


def test_database_init(app):
    from api.database import Database

    db = Database(app)
    assert db.app == app
