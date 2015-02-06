# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""
from flask.ext.restful import Api
from flask_restful_swagger import swagger

restapi = swagger.docs(Api(),
                    apiVersion='0.1',
                    api_spec_url='/api/spec',
                    description='gluu cluster API')
