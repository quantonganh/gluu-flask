# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2015 Gluu
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
import time

from api.setup.base import BaseSetup


class OxTrustSetup(BaseSetup):
    def setup(self):
        start = time.time()
        self.logger.info("oxTrust setup is started")

        # generate oxtrustLdap.properties, oxTrust.properties,
        # oxauth-static-conf.json, oxTrustLogRotationConfiguration.xml,
        # self.copy_tomcat_conf()

        # Create or copy key material to /etc/certs
        # self.gen_cert()

        # Configure apache httpd to proxy AJP:8009

        # Configure tomcat to run oxtrust war file

        elapsed = time.time() - start
        self.logger.info("oxTrust setup is finished ({} seconds)".format(elapsed))
