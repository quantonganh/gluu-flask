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

@swagger.model
class Cluster:
    def __init__(self, install_dir=None):
        self.log = '%s/setup.log' % self.install_dir
        self.logError = '%s/setup_error.log' % self.install_dir

        self.gluuOptFolder = "/opt/gluu"
        self.gluuOptBinFolder = "/opt/gluu/bin"
        self.configFolder = '/etc/gluu/config'
        self.certFolder = '/etc/certs'
        self.tomcatHome = '/opt/tomcat'
        self.tomcat_user_home_lib = "/home/tomcat/lib"
        self.oxauth_lib = "/opt/tomcat/webapps/oxauth/WEB-INF/lib"
        self.tomcatWebAppFolder = "/opt/tomcat/webapps"
        self.oxBaseDataFolder = "/var/ox"
        self.oxPhotosFolder = "/var/ox/photos"
        self.oxTrustRemovedFolder = "/var/ox/oxtrust/removed"
        self.etc_hosts = '/etc/hosts'
        self.etc_hostname = '/etc/hostname'

        self.idpFolder = "/opt/idp"
        self.idpMetadataFolder = "/opt/idp/metadata"
        self.idpLogsFolder = "/opt/idp/logs"
        self.idpLibFolder = "/opt/idp/lib"
        self.idpConfFolder = "/opt/idp/conf"
        self.idpSslFolder = "/opt/idp/ssl"
        self.idpTempMetadataFolder = "/opt/idp/temp_metadata"
        self.idpWarFolder = "/opt/idp/war"
        self.idpSPFolder = "/opt/idp/sp"

        self.hostname = None
        self.ip = None
        self.orgName = None
        self.orgShortName = None
        self.countryCode = None
        self.city = None
        self.state = None
        self.admin_email = None
        self.encoded_ox_ldap_pw = None
        self.encoded_ldap_pw = None
        self.encoded_shib_jks_pw = None
        self.oxauthClient_encoded_pw = None
        self.baseInum = None
        self.inumOrg = None
        self.inumAppliance = None
        self.inumOrgFN = None
        self.inumApplianceFN = None
        self.oxTrustConfigGeneration = "disabled"
        self.ldapBaseFolderldapPass = None
        self.oxauth_client_id = None
        self.oxauthClient_pw = None
        self.encode_salt = "123456789012345678901234"

        self.outputFolder = '%s/output' % self.install_dir
        self.templateFolder = '%s/templates' % self.install_dir
        self.staticFolder = '%s/static/opendj' % self.install_dir
        self.indexJson = '%s/static/opendj/opendj_index.json' % self.install_dir
        self.oxauth_error_json = '%s/static/oxauth/oxauth-errors.json' % self.install_dir

        self.httpdKeyPass = None
        self.httpdKeyFn = '%s/httpd.key' % self.certFolder
        self.httpdCertFn = '%s/httpd.crt' % self.certFolder
        self.shibJksPass = None
        self.shibJksFn = '%s/shibIDP.jks' % self.certFolder
        self.asimbaJksPass = None
        self.asimbaJksFn = '%s/asimbaIDP.jks' % self.certFolder
        self.openDjCertFn = '%s/opendj.crt' % self.certFolder

        self.ldap_type = "opendj"
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
        self.gluuScriptFiles = ['%s/static/scripts/logmanager.sh' % self.install_dir,
                                '%s/static/scripts/testBind.py' % self.install_dir]
        self.init_files = ['%s/static/tomcat/tomcat' % self.install_dir,
                           '%s/static/opendj/opendj' % self.install_dir]
        self.redhat_services = ['memcached', 'opendj', 'tomcat', 'httpd']
        self.debian_services = [{ 'name' : 'memcached', 'order' : '30', 'runlevel' : '3'},
                                { 'name' : 'opendj', 'order' : '40', 'runlevel' : '3'},
                                { 'name' : 'opendj', 'order' : '40', 'runlevel' : '3'},
                                { 'name' : 'tomcat', 'order' : '50', 'runlevel' : '3'},
                                { 'name' : 'apache2', 'order' : '60', 'runlevel' : '3'}]

        self.ldap_start_script = '/etc/init.d/opendj'
        self.apache_start_script = '/etc/init.d/httpd'
        self.tomcat_start_script = '/etc/init.d/tomcat'

        self.ldapEncodePWCommand = '%s/bin/encode-password' % self.ldapBaseFolder
        self.oxEncodePWCommand = '%s/bin/encode.py' % self.gluuOptFolder
        self.keytoolCommand = '/usr/java/latest/bin/keytool'
        self.jarCommand = '/usr/bin/jar'
        self.opensslCommand = '/usr/bin/openssl'
        self.defaultTrustStoreFN = '/usr/java/latest/lib/security/cacerts'
        self.defaultTrustStorePW = 'changeit'

        self.oxtrust_openid_client_id = None
        self.oxtrust_uma_client_id = None

        # Stuff that gets rendered; filname is necessary. Full path should
        # reflect final path if the file must be copied after its rendered.
        self.oxauth_ldap_properties = '%s/conf/oxauth-ldap.properties' % self.tomcatHome
        self.oxauth_config_xml = '%s/conf/oxauth-config.xml' % self.tomcatHome
        self.oxTrust_properties = '%s/conf/oxTrust.properties' % self.tomcatHome
        self.tomcat_server_xml = '%s/conf/server.xml' % self.tomcatHome
        self.oxtrust_ldap_properties = '%s/conf/oxTrustLdap.properties' % self.tomcatHome
        self.tomcat_gluuTomcatWrapper = '%s/conf/gluuTomcatWrapper.conf' % self.tomcatHome
        self.tomcat_oxauth_static_conf_json = '%s/conf/oxauth-static-conf.json' % self.tomcatHome
        self.tomcat_log_folder = "%s/logs" % self.tomcatHome
        self.tomcat_max_ram = None    # in MB
        self.oxTrust_log_rotation_configuration = "%s/conf/oxTrustLogRotationConfiguration.xml" % self.tomcatHome
        self.eduperson_schema_ldif = '%s/config/schema/96-eduperson.ldif'
        self.apache2_conf = '%s/httpd.conf' % self.outputFolder
        self.apache2_ssl_conf = '%s/https_gluu.conf' % self.outputFolder
        self.ldif_base = '%s/base.ldif' % self.outputFolder
        self.ldif_appliance = '%s/appliance.ldif' % self.outputFolder
        self.ldif_attributes = '%s/attributes.ldif' % self.outputFolder
        self.ldif_scopes = '%s/scopes.ldif' % self.outputFolder
        self.ldif_clients = '%s/clients.ldif' % self.outputFolder
        self.ldif_people = '%s/people.ldif' % self.outputFolder
        self.ldif_groups = '%s/groups.ldif' % self.outputFolder
        self.ldif_site = '%s/static/cache-refresh/o_site.ldif' % self.install_dir
        self.ldif_scripts = '%s/scripts.ldif' % self.outputFolder
        self.encode_script = '%s/bin/encode.py' % self.gluuOptFolder
        self.cas_properties = '%s/cas.properties' % self.outputFolder
        self.asimba_configuration = '%s/asimba.xml' % self.outputFolder
        self.asimba_selector_configuration = '%s/conf/asimba-selector.xml' % self.tomcatHome

        self.ldap_setup_properties = '%s/opendj-setup.properties' % self.templateFolder

        self.ldif_files = [self.ldif_base,
                           self.ldif_appliance,
                           self.ldif_attributes,
                           self.ldif_scopes,
                           self.ldif_clients,
                           self.ldif_people,
                           self.ldif_groups,
                           self.ldif_site,
                           self.ldif_scripts]

        self.ce_templates = {self.oxauth_ldap_properties: True,
                             self.oxauth_config_xml: True,
                             self.oxTrust_properties: True,
                             self.tomcat_server_xml: True,
                             self.oxtrust_ldap_properties: True,
                             self.tomcat_gluuTomcatWrapper: True,
                             self.tomcat_oxauth_static_conf_json: True,
                             self.oxTrust_log_rotation_configuration: True,
                             self.ldap_setup_properties: False,
                             self.org_custom_schema: False,
                             self.apache2_conf: False,
                             self.apache2_ssl_conf: False,
                             self.etc_hosts: False,
                             self.etc_hostname: False,
                             self.ldif_base: False,
                             self.ldif_appliance: False,
                             self.ldif_attributes: False,
                             self.ldif_scopes: False,
                             self.ldif_clients: False,
                             self.ldif_people: False,
                             self.ldif_groups: False,
                             self.ldif_scripts: False,
                             self.cas_properties: False,
                             self.asimba_configuration: False,
                             self.asimba_selector_configuration: True
        }

"""An object to model the cluster """
    def __init__(self):
        pass