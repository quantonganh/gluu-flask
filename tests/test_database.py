import pytest


class DummyObject(object):
    pass


DummyTableName = DummyObject()
DummyTableName.__table_name__ = "dummy_table_name"


@pytest.mark.parametrize("obj, expected", [
    (DummyObject(), "dummyobject"),
    (DummyObject, "dummyobject"),
    (DummyTableName, "dummy_table_name"),
])
def test_table_from_obj(obj, expected):
    from api.database import _table_name_from_obj
    assert expected == _table_name_from_obj(obj)


def test_database_init(app):
    from api.database import Database

    db = Database(app)
    assert db.app == app
