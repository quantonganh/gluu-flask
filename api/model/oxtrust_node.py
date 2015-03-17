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
from flask_restful_swagger import swagger
from flask.ext.restful import fields

from .base import BaseModel


@swagger.model
class oxtrustNode(BaseModel):
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
        self.hostname = ""
        self.ip = ""
        self.type = "oxtrust"

        self.tomcat_home = "/opt/tomcat"
        self.tomcat_conf_dir = "/opt/tomcat/conf"
        self.tomcat_log_folder = "/opt/tomcat/logs"
        self.ldap_binddn = 'cn=directory manager'
        self.openssl_cmd = "/usr/bin/openssl"
        self.cert_folder = "/etc/certs"
        self.httpd_key = "/etc/certs/httpd.key"
        self.httpd_key_orig = "/etc/certs/httpd.key.orig"
        self.httpd_csr = "/etc/certs/httpd.csr"
        self.httpd_crt = "/etc/certs/httpd.crt"
        self.defaultTrustStoreFN = '/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/security/cacerts'

        self.shib_jks_pass = ""
        self.encoded_shib_jks_pw = ""
        self.shib_jks_fn = "/etc/certs/shibIDP.jks"

        # enabled if we have saml
        self.oxtrust_config_generation = "disabled"
        self.oxauth_client_id = ""

        self.ldapPass = ""
        self.encoded_ox_ldap_pw = ""
        self.oxauth_client_pw = ""
        self.oxauth_client_encoded_pw = ""

        # these templates should be rendered and copied to tomcat
        # conf directory
        self.oxtrust_properties = "api/templates/salt/oxtrust/oxTrust.properties"
        self.oxtrust_ldap_properties = "api/templates/salt/oxtrust/oxTrustLdap.properties"
        self.oxtrust_log_rotation_configuration = "api/templates/salt/oxtrust/oxTrustLogRotationConfiguration.xml"
        self.oxauth_static_conf_json = "api/templates/salt/_shared/oxauth-static-conf.json"

        # the following template should be rendered and copied
        # to apache2 conf directory
        self.apache2_ssl_conf = "api/templates/salt/_shared/https_gluu.conf"

        # the following template should be copied to
        # /opt/tomcat/conf/template/conf
        self.oxtrust_cache_refresh_properties = "api/templates/salt/oxtrust/oxTrustCacheRefresh-template.properties.vm"
