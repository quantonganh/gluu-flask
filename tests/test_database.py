def test_database_init(app):
    from api.database import Database

    db = Database(app)
    assert db.app == app
