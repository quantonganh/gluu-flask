#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from api.app import create_app
from api.settings import DevConfig, ProdConfig

if os.environ.get("API_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

if __name__ == '__main__':
    app.run(port = app.config['PORT'])
