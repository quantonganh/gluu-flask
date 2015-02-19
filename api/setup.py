# -*- coding: utf-8 -*-
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

class ldapSetup(object):
    def setup(self):
        if not self.id and self.name and self.type:
            print "log: node is not defined properly"
            return None
        saltlocal = salt.client.LocalClient()
        with open(self.ldapPassFn, 'w') as fp:
            fp.write(self.ldapPass)
        for ldif in self.ldif_files:
            with open(ldif, 'r') as fp:
                tmpl = fp.read()
            with open(self.outputFolder + ldif, 'w') as fp:
                fp.write(tmpl % self.__dict__)
            saltlocal.cmd(self.id, 'cp.get_file', [self.outputFolder + ldif, target]) #where is terget???
        #setup_opendj
        for schemaFile in self.schemaFiles:
            saltlocal.cmd(self.id, 'cp.get_file', [schemaFile, self.schemaFolder])
        setupPropsFN = os.path.join(self.ldapBaseFolder, 'opendj-setup.properties')
        saltlocal.cmd(self.id, 'cp.get_file', ["%s/opendj-setup.properties" % self.outputFolder, setupPropsFN])
        saltlocal.cmd(self.id, 'cmd.run', [" ".join([self.ldapSetupCommand,
                                '--no-prompt',
                                '--cli',
                                '--propertiesFilePath',
                                setupPropsFN,
                                '--acceptLicense'])])
        saltlocal.cmd(self.id, 'cmd.run', [self.ldapDsJavaPropCommand])
        #configure_opendj
        config_changes = [['set-global-configuration-prop', '--set', 'single-structural-objectclass-behavior:accept'],
                          ['set-attribute-syntax-prop', '--syntax-name', '"Directory String"',   '--set', 'allow-zero-length-values:true'],
                          ['set-password-policy-prop', '--policy-name', '"Default Password Policy"', '--set', 'allow-pre-encoded-passwords:true'],
                          ['set-log-publisher-prop', '--publisher-name', '"File-Based Audit Logger"', '--set', 'enabled:true'],
                          ['create-backend', '--backend-name', 'site', '--set', 'base-dn:o=site', '--type local-db', '--set', 'enabled:true']]
        for changes in config_changes:
            dsconfigCmd = " ".join(['cd %s/bin ; ' % self.ldapBaseFolder,
                                    self.ldapDsconfigCommand,
                                    '--trustAll',
                                    '--no-prompt',
                                    '--hostname',
                                    self.ldap_hostname,
                                    '--port',
                                    self.ldap_admin_port,
                                    '--bindDN',
                                    '"%s"' % self.ldap_binddn,
                                    '--bindPasswordFile',
                                    self.ldapPassFn] + changes)
            saltlocal.cmd(self.id, 'cmd.run', [dsconfigCmd])
        #index_opendj
        index_json = self.load_json(self.indexJson)
        if index_json:
            for attrDict in index_json:
                attr_name = attrDict['attribute']
                index_types = attrDict['index']
                for index_type in index_types:
                    self.logIt("Creating %s index for attribute %s" % (index_type, attr_name))
                    indexCmd = " ".join(['cd %s/bin ; ' % self.ldapBaseFolder,
                                         self.ldapDsconfigCommand,
                                         'create-local-db-index',
                                         '--backend-name',
                                         'userRoot',
                                         '--type',
                                         'generic',
                                         '--index-name',
                                         attr_name,
                                         '--set',
                                         'index-type:%s' % index_type,
                                         '--set',
                                         'index-entry-limit:4000',
                                         '--hostName',
                                         self.ldap_hostname,
                                         '--port',
                                         self.ldap_admin_port,
                                         '--bindDN',
                                         '"%s"' % self.ldap_binddn,
                                         '-j', self.ldapPassFn,
                                         '--trustAll',
                                         '--noPropertiesFile',
                                         '--no-prompt'])
                    saltlocal.cmd(self.id, 'cmd.run', [indexCmd])
        #import_ldif

class nodeSetup(object):
    def __init__(self, node = None):
        self.d = {
            'gluuopendj' : ldapSetup,
            #'gluuoxauth' : oxauthSetup,
            #'gluuoxtrust' : oxtrustSetup,
        }
        if node:
            self.node = node
            self.so = d[node.type]()

    def setup(self):
        self.so.setup(self.node)