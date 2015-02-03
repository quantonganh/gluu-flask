#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.testing import TestCase
from api.settings import TestConfig
from api.app import create_app as test_app
from flask.ext import restful
from api.resources import Bootstrap
import json

class TestApis(TestCase):

    def create_app(self):
        app = test_app(TestConfig)
        restapi = restful.Api(app)
        restapi.add_resource(Bootstrap, '/bootstrap')
        return app

    def test_bootstrap_get(self):
        response = self.client.get("/bootstrap")
        self.assertEquals(json.loads(response.data), dict(echo = 'list docker image ids and container ids'))
