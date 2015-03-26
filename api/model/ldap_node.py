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
from flask_restful_swagger import swagger
from flask.ext.restful import fields

from api.model.base import BaseModel
from api.helper.common_helper import generate_passkey
from api.helper.common_helper import decrypt_text
from api.helper.common_helper import encrypt_text
from api.helper.common_helper import get_random_chars


@swagger.model
class ldapNode(BaseModel):
    # Swager Doc
    resource_fields = {
        'id': fields.String(attribute='Node unique identifier'),
        'type': fields.String(attribute='Node type'),
        'cluster_id': fields.String(attribute='Cluster ID'),
        'local_hostname': fields.String(attribute='Local hostname of the node (not the cluster hostname).'),
        'ip': fields.String(attribute='IP address of the node'),
        'ldap_binddn': fields.String(attribute='LDAP super user Bind DN. Probably should leave it default cn=directory manager.'),
        'ldap_port': fields.String(attribute='Non SSL LDAP port (not used)'),
        'ldaps_port': fields.String(attribute='LDAPS port'),
        'ldap_admin_port': fields.String(attribute='Admin port'),
        'ldap_jmx_port': fields.String(attribute='JMX port (not used)'),
    }

    def __init__(self):
        self.install_dir = ""
        self.ldap_type = "opendj"

        self.local_hostname = ""
        self.ip = ""

        # Filesystem path of the opendj-setup.properties template
        self.ldap_setup_properties = "api/templates/salt/opendj/opendj-setup.properties"

        # Filesystem path of the public certificate for OpenDJ
        self.openDjCertFn = '/etc/certs/opendj.crt'

        self.ldap_binddn = 'cn=directory manager'
        self.ldap_port = '1389'
        self.ldaps_port = '1636'
        self.ldap_jmx_port = '1689'
        self.ldap_admin_port = '4444'
        self.ldap_replication_port = "8989"

        # Where to install OpenDJ, usually /opt/opendj
        self.ldapBaseFolder = '/opt/opendj'

        # How long to wait for LDAP to start
        self.ldapStartTimeOut = 30

        # Full path to opendj setup command
        self.ldapSetupCommand = '%s/setup' % self.ldapBaseFolder

        # Full path to dsconfig command
        self.ldapDsconfigCommand = "%s/bin/dsconfig" % self.ldapBaseFolder

        # Full path to create-rc command
        self.ldapDsCreateRcCommand = "%s/bin/create-rc-script" % self.ldapBaseFolder

        # Full path to dsjavaproperties command
        self.ldapDsJavaPropCommand = "%s/bin/dsjavaproperties" % self.ldapBaseFolder

        # Full path to import command
        self.importLdifCommand = '%s/bin/import-ldif' % self.ldapBaseFolder

        # Full path to encode password
        self.ldapEncodePWCommand = '%s/bin/encode-password' % self.ldapBaseFolder

        # Temporary path to store ldap password (should be removed)
        self.ldapPassFn = '/home/ldap/.pw'

        # Full path of template schema to copy to the opendj server
        self.schemaFolder = "%s/template/config/schema" % self.ldapBaseFolder
        self.org_custom_schema = "%s/config/schema/100-user.ldif" % self.ldapBaseFolder
        self.schemaFiles = [
            "api/templates/salt/opendj/schema/101-ox.ldif",
            "api/templates/salt/opendj/schema/77-customAttributes.ldif",
            "api/templates/salt/opendj/schema/96-eduperson.ldif",
            "api/templates/salt/opendj/schema/100-user.ldif",
        ]

        # Full path of template init file
        self.init_file = '%s/static/opendj/opendj' % self.install_dir

        # Full path of the destination of the init script
        self.ldap_start_script = '/etc/init.d/opendj'

        # Full path to java keytool command
        self.keytoolCommand = '/usr/bin/keytool'
        # self.keytoolCommand = '/usr/java/latest/bin/keytool'

        # Full path to openssl command
        self.opensslCommand = '/usr/bin/openssl'

        self.outputFolder = '/tmp'

        self.ldif_base = 'api/templates/salt/opendj/ldif/base.ldif'
        self.ldif_appliance = 'api/templates/salt/opendj/ldif/appliance.ldif'
        self.ldif_attributes = 'api/templates/salt/opendj/ldif/attributes.ldif'
        self.ldif_scopes = 'api/templates/salt/opendj/ldif/scopes.ldif'
        self.ldif_clients = 'api/templates/salt/opendj/ldif/clients.ldif'
        self.ldif_people = 'api/templates/salt/opendj/ldif/people.ldif'
        self.ldif_groups = 'api/templates/salt/opendj/ldif/groups.ldif'
        self.ldif_site = 'api/templates/salt/opendj/ldif/o_site.ldif'
        self.ldif_scripts = 'api/templates/salt/opendj/ldif/scripts.ldif'

        # List of initial ldif files
        self.ldif_files = [
            self.ldif_base,
            self.ldif_appliance,
            self.ldif_attributes,
            self.ldif_scopes,
            self.ldif_clients,
            self.ldif_people,
            self.ldif_groups,
            self.ldif_site,
            self.ldif_scripts,
        ]

        self.id = ''
        self.name = ''
        self.type = 'ldap'
        self.cluster_name = ""
        self.defaultTrustStoreFN = '/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/security/cacerts'
        self.indexJson = "api/templates/salt/opendj/opendj_index.json"

        self.passkey = generate_passkey()
        self.ldapPass = encrypt_text(get_random_chars(), self.passkey)
        # self.encoded_ldap_pw = ""
        self.encoded_ox_ldap_pw = ""
        # not sure whether these attrs belong this model or oxauthNode
        self.oxauth_client_id = ""
        self.oxauth_client_pw = ""
        self.oxauth_client_encoded_pw = ""

    @property
    def decrypted_ldap_pw(self):
        return decrypt_text(self.ldapPass, self.passkey)
