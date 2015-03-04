#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from crochet import setup as crochet_setup

from api.app import create_app
from api.settings import DevConfig, ProdConfig

if os.environ.get("API_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)


@app.before_first_request
def bootstrap():
    if not app.config["SALT_MASTER_IPADDR"]:
        raise RuntimeError("Unable to get salt-master IP address. "
                           "Make sure the SALT_MASTER_IPADDR "
                           "environment variable is set.")


if __name__ == '__main__':
    crochet_setup()
    app.run(port=app.config['PORT'])
