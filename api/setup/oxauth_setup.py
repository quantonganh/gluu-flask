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
import codecs
import os.path
import shutil
import time

from api.helper.common_helper import run
from api.helper.common_helper import get_random_chars
from api.setup.base import BaseSetup


class OxAuthSetup(BaseSetup):
    def copy_tomcat_conf(self):
        # static template
        self.logger.info("copying {}".format(self.node.oxauth_errors_json))
        run("salt-cp {} {} {}".format(
            self.node.id,
            self.node.oxauth_errors_json,
            os.path.join(
                self. node.tomcat_conf_dir,
                os.path.basename(self.node.oxauth_errors_json),
            ),
        ))

        ctx = {
            "inumOrg": self.cluster.inumOrg,
            "ldaps_port": self.cluster.ldaps_port,
            "certFolder": self.node.cert_folder,
            "hostname": self.node.hostname,
            "inumAppliance": self.cluster.inumAppliance,
            "ldap_binddn": self.node.ldap_binddn,
            "encoded_ox_ldap_pw": self.node.encoded_ox_ldap_pw,

            # FIXME: the following keys are left blank
            #        it will be populated eventually
            "ldap_hostname": "",
        }

        # rendered templates
        conf_templates = (
            self.node.oxauth_ldap_properties,
            self.node.oxauth_config_xml,
            self.node.oxauth_static_conf_json,
            # self.tomcat_server_xml,
        )
        for tmpl in conf_templates:
            rendered_content = ""
            try:
                with codecs.open(tmpl, "r", encoding="utf-8") as fp:
                    rendered_content = fp.read() % ctx
            except Exception as exc:
                self.logger.error(exc)

            file_basename = os.path.basename(tmpl)
            local_dest = os.path.join(self.build_dir, file_basename)
            remote_dest = os.path.join(self.node.tomcat_conf_dir, file_basename)

            try:
                with codecs.open(local_dest, "w", encoding="utf-8") as fp:
                    fp.write(rendered_content)
            except Exception as exc:
                self.logger.error(exc)

            self.logger.info("copying {}".format(local_dest))
            run("salt-cp {} {} {}".format(self.node.id, local_dest,
                                          remote_dest))

    def gen_cert(self):
        passwd = get_random_chars()
        suffix = "httpd"
        user = "apache"

        mkdir_cmd = "mkdir -p {}".format(self.node.cert_folder)

        # command to create key with password file
        keypass_cmd = " ".join([self.node.openssl_cmd, "genrsa", "-des3",
                                "-out", self.node.httpd_key_orig,
                                "-passout", "pass:{}".format(passwd), "2048"])

        # command to create key file
        key_cmd = " ".join([self.node.openssl_cmd, "rsa", "-in",
                            self.node.httpd_key_orig, "-passin",
                            "pass:{}".format(passwd), "-out", self.node.httpd_key])

        # command to create csr file
        csr_cmd = " ".join([self.node.openssl_cmd, "req", "-new",
                            "-key", self.node.httpd_key, "-out", self.node.httpd_csr,
                            "-subj", "/CN=%s/O=%s/C=%s/ST=%s/L=%s" % (
                                self.node.hostname,
                                self.cluster.orgName,
                                self.cluster.countryCode,
                                self.cluster.state,
                                self.cluster.city,
                            )])

        # command to create crt file
        crt_cmd = " ".join([self.node.openssl_cmd, "x509", "-req",
                            "-days", "365",
                            "-in", self.node.httpd_csr,
                            "-signkey", self.node.httpd_key,
                            "-out", self.node.httpd_crt])

        self.logger.info("generating certificates for {}".format(suffix))
        self.saltlocal.cmd(
            self.node.id,
            ["cmd.run", "cmd.run", "cmd.run", "cmd.run", "cmd.run"],
            [[mkdir_cmd], [keypass_cmd], [key_cmd], [csr_cmd], [crt_cmd]],
        )

        self.logger.info("changing access to certificates")
        self.saltlocal.cmd(
            self.node.id,
            ["cmd.run", "cmd.run", "cmd.run", "cmd.run"],
            [
                ["/bin/chown {0}:{0} {1}".format(user, self.node.httpd_key_orig)],
                ["/bin/chmod 700 {}".format(self.node.httpd_key_orig)],
                ["/bin/chown {0}:{0} {1}".format(user, self.node.httpd_key)],
                ["/bin/chmod 700 {}".format(self.node.httpd_key)],
            ],
        )

        import_cmd = " ".join(["/usr/bin/keytool", "-import", "-trustcacerts",
                               "-alias", "{}_{}".format(self.node.hostname, suffix),
                               "-file", self.node.httpd_crt,
                               "-keystore", self.node.defaultTrustStoreFN,
                               "-storepass", "changeit", "-noprompt"])

        self.logger.info("importing public certificate into Java truststore")
        self.saltlocal.cmd(self.node.id, "cmd.run", [import_cmd])

        # TODO: generate OpenID keys; see http://git.io/pMJE
        self.logger.info("changing access to {}".format(self.node.cert_folder))
        self.saltlocal.cmd(
            self.node.id,
            ["cmd.run", "cmd.run"],
            [["/bin/chown -R tomcat:tomcat {}".format(self.node.cert_folder)],
             ["/bin/cmhmod -R 500 {}".format(self.node.cert_folder)]],
        )

    def copy_httpd_conf(self):
        ctx = {
            "hostname": self.node.hostname,
            "ip": self.node.ip,
            "httpdCertFn": self.node.httpd_crt,
            "httpdKeyFn": self.node.httpd_key,
        }

        tmpl = self.node.apache2_ssl_conf
        rendered_content = ""

        self.saltlocal.cmd(
            self.node.id,
            ["cmd.run", "cmd.run"],
            [
                ["mkdir -p /etc/apache2/sites-available"],
                ["mkdir -p /etc/apache2/sites-enabled"],
            ],
        )

        try:
            with codecs.open(tmpl, "r", encoding="utf-8") as fp:
                rendered_content = fp.read() % ctx
        except Exception as exc:
            self.logger.error(exc)

        file_basename = os.path.basename(tmpl)
        local_dest = os.path.join(self.build_dir, file_basename)
        remote_dest = os.path.join("/etc/apache2/sites-available",
                                   file_basename)

        try:
            with codecs.open(local_dest, "w", encoding="utf-8") as fp:
                fp.write(rendered_content)
        except Exception as exc:
            self.logger.error(exc)

        self.logger.info("copying {}".format(local_dest))
        run("salt-cp {} {} {}".format(self.node.id, local_dest,
                                      remote_dest))

        # TODO: when to run httpd service?
        symlink_cmd = "ln -s /etc/apache2/sites-available/{0} " \
                      "/etc/apache2/sites-enabled/{0}".format(file_basename)
        self.logger.info("symlinking {}".format(file_basename))
        self.saltlocal.cmd(self.node.id, "cmd.run", [symlink_cmd])

    def setup(self):
        start = time.time()

        self.logger.info("oxAuth setup is started")
        # copy rendered templates: oxauth-ldap.properties,
        # oxauth-config.xml, oxauth-static-conf.json
        self.copy_tomcat_conf()

        # create or copy key material to /etc/certs
        self.gen_cert()

        # configure apache httpd to proxy AJP:8009
        self.copy_httpd_conf()

        # TODO: configure tomcat to run oxauth war file

        # cleanup build directory
        shutil.rmtree(self.build_dir)
        elapsed = time.time() - start
        self.logger.info("oxAuth setup is finished ({} seconds)".format(elapsed))
        return True
