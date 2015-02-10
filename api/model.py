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
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from flask_restful_swagger import swagger
import os
import os.path
import json
from api.settings import Config

@swagger.model
class cluster:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.description = ""
        self.ldap_nodes = {}
        self.oxauth_nodes = {}
        self.oxtrust_nodes = {}
        self.hostname_ldap_cluster = ""
        self.hostname_oxauth_cluster = ""
        self.hostname_oxtrust_cluster = ""

        # X.509 Certificate Information
        self.orgName = None
        self.orgShortName = None
        self.countryCode = None
        self.city = None
        self.state = None
        self.admin_email = None

        # Cluster secrets
        self.encoded_ox_ldap_pw = None
        self.encoded_ldap_pw = None
        self.oxauthClient_encoded_pw = None

        # Inums
        self.baseInum = None
        self.inumOrg = None
        self.inumAppliance = None
        self.inumOrgFN = None
        self.inumApplianceFN = None

    def persist(self):
        db = Config.DB
        if not os.path.exists(db):
            os.mkdir(db)
        jsonData = json.dumps(self.__dict__)
        with open('%s/cluster%s.json' % (db, self.id), 'w') as outfile:
            json.dump(jsonData, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

@swagger.model
class ldapNode:
    def __init__(self, install_dir=None):
        self.local_hostname = None
        self.ip = None
        self.ldap_setup_properties = './templates/opendj-setup.properties'
        self.ldap_type = "opendj"
        self.openDjCertFn = '/etc/certs/opendj.crt'
        self.ldap_binddn = 'cn=directory manager'
        self.ldap_hostname = "localhost"
        self.ldap_port = '1389'
        self.ldaps_port = '1636'
        self.ldap_jmx_port = '1689'
        self.ldap_admin_port = '4444'
        self.ldapBaseFolder = '/opt/opendj'
        self.ldapStartTimeOut = 30
        self.ldapSetupCommand = '%s/setup' % self.ldapBaseFolder
        self.ldapDsconfigCommand = "%s/bin/dsconfig" % self.ldapBaseFolder
        self.ldapDsCreateRcCommand = "%s/bin/create-rc-script" % self.ldapBaseFolder
        self.ldapDsJavaPropCommand = "%s/bin/dsjavaproperties" % self.ldapBaseFolder
        self.ldapPassFn = '/home/ldap/.pw'
        self.importLdifCommand = '%s/bin/import-ldif' % self.ldapBaseFolder
        self.schemaFolder = "%s/template/config/schema" % self.ldapBaseFolder
        self.org_custom_schema = "%s/config/schema/100-user.ldif" % self.ldapBaseFolder
        self.schemaFiles = ["%s/static/%s/96-eduperson.ldif" % (self.install_dir, self.ldap_type),
                            "%s/static/%s/101-ox.ldif" % (self.install_dir, self.ldap_type),
                            "%s/static/%s/77-customAttributes.ldif" % (self.install_dir, self.ldap_type),
                            "%s/output/100-user.ldif" % self.install_dir]
        self.init_file = '%s/static/opendj/opendj' % self.install_dir
        self.ldap_start_script = '/etc/init.d/opendj'

        self.ldapEncodePWCommand = '%s/bin/encode-password' % self.ldapBaseFolder
        self.keytoolCommand = '/usr/java/latest/bin/keytool'
        self.opensslCommand = '/usr/bin/openssl'

        self.ldif_base = '%s/base.ldif' % self.outputFolder
        self.ldif_appliance = '%s/appliance.ldif' % self.outputFolder
        self.ldif_attributes = '%s/attributes.ldif' % self.outputFolder
        self.ldif_scopes = '%s/scopes.ldif' % self.outputFolder
        self.ldif_clients = '%s/clients.ldif' % self.outputFolder
        self.ldif_people = '%s/people.ldif' % self.outputFolder
        self.ldif_groups = '%s/groups.ldif' % self.outputFolder
        self.ldif_site = '%s/static/cache-refresh/o_site.ldif' % self.install_dir
        self.ldif_scripts = '%s/scripts.ldif' % self.outputFolder
        self.ldif_files = [self.ldif_base,
                           self.ldif_appliance,
                           self.ldif_attributes,
                           self.ldif_scopes,
                           self.ldif_clients,
                           self.ldif_people,
                           self.ldif_groups,
                           self.ldif_site,
                           self.ldif_scripts]
