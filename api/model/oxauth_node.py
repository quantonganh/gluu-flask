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
from flask_restful_swagger import swagger
from flask.ext.restful import fields

from api.model.base import BaseModel


@swagger.model
class oxauthNode(BaseModel):
    # Swager Doc
    resource_fields = {
        "id": fields.String(attribute="Node unique identifier"),
        "name": fields.String(attribute="Node name"),
        "type": fields.String(attribute="Node type"),
        "ip": fields.String(attribute="Node IP address"),
        "cluster_id": fields.String(attribute="Cluster ID"),
    }

    def __init__(self):
        self.id = ""
        self.cluster_id = ""
        self.name = ""
        self.ip = ""
        self.type = "oxauth"

        self.defaultTrustStoreFN = '/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/security/cacerts'
        self.ldap_binddn = 'cn=directory manager'

        self.tomcat_home = "/opt/tomcat"
        self.tomcat_conf_dir = "/opt/tomcat/conf"

        self.openssl_cmd = "/usr/bin/openssl"
        self.cert_folder = "/etc/certs"
        self.httpd_key = "/etc/certs/httpd.key"
        self.httpd_key_orig = "/etc/certs/httpd.key.orig"
        self.httpd_csr = "/etc/certs/httpd.csr"
        self.httpd_crt = "/etc/certs/httpd.crt"

        self.oxauth_lib = "/opt/tomcat/webapps/oxauth/WEB-INF/lib"

        # the following template should be copied to tomcat conf directory
        self.oxauth_errors_json = "api/templates/salt/oxauth/oxauth-errors.json"

        # the following templates should be rendered and copied
        # to tomcat conf directory
        self.oxauth_ldap_properties = "api/templates/salt/oxauth/oxauth-ldap.properties"
        self.oxauth_config_xml = "api/templates/salt/oxauth/oxauth-config.xml"
        self.oxauth_static_conf_json = "api/templates/salt/_shared/oxauth-static-conf.json"
        self.tomcat_server_xml = "api/templates/salt/oxauth/server.xml"

        # the following template should be rendered and copied
        # to apache2 conf directory
        self.apache2_ssl_conf = "api/templates/salt/_shared/https_gluu.conf"
