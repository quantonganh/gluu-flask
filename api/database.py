# The MIT License (MIT)
#
# Copyright (c) 2014 Gluu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os

import jsonpickle
import tinydb


def _table_name_from_obj(obj):
    table_name = None
    if isinstance(obj, str):
        table_name = obj
    elif hasattr(obj, "__table_name__"):
        table_name = obj.__table_name__

    assert table_name is not None, "At least a string or object " \
                                   "with __table_name__ attribute " \
                                   "is required"
    return table_name


class Database(object):
    def __init__(self, app=None):
        self._db = None
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("DATABASE_URI", "")
        app.extensions = getattr(app, "extensions", {})
        app.extensions["tinydb"] = self
        self.app = app

    @property
    def db(self):
        assert self.app, "The tinydb extension is not registered in current " \
                         "application. Ensure you have called init_app first."

        if not self._db:
            try:
                os.makedirs(os.path.dirname(self.app.config["DATABASE_URI"]))
            except OSError:
                pass
            self._db = tinydb.TinyDB(self.app.config["DATABASE_URI"])
        return self._db

    def get(self, identifier, obj):
        _obj = None

        table_name = _table_name_from_obj(obj)
        table = self.db.table(table_name)
        data = table.get(tinydb.where("id") == identifier)

        if data:
            _obj = jsonpickle.decode(json.dumps(data))
        return _obj

    def persist(self, obj):
        # encode the object so we can decode it later
        encoded = jsonpickle.encode(obj)

        # tinydb requires a ``dict`` object
        data = json.loads(encoded)

        table_name = _table_name_from_obj(obj)
        table = self.db.table(table_name)
        table.insert(data)
        return True

    def all(self, obj):
        table_name = _table_name_from_obj(obj)
        table = self.db.table(table_name)
        data = table.all()
        return [jsonpickle.decode(json.dumps(item)) for item in data]

    def delete(self, identifier, obj):
        table_name = _table_name_from_obj(obj)
        table = self.db.table(table_name)
        table.remove(tinydb.where("id") == identifier)
        return True

    def update(self, obj):
        # encode the object so we can decode it later
        encoded = jsonpickle.encode(obj)

        # tinydb requires a ``dict`` object
        data = json.loads(encoded)

        table_name = _table_name_from_obj(obj)
        table = self.db.table(table_name)
        table.update(data, tinydb.where("id") == obj.id)
        return True


# shortcut to database object
db = Database()
