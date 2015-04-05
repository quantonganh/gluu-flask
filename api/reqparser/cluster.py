import re

from flask.ext.restful import reqparse

# regex pattern to validate email address
EMAIL_RE_ = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def country_code(value, name):
    if len(value) == 2:
        return value
    raise ValueError("The parameter {} requires 2 letters value".format(name))


def admin_email(value, name):
    if EMAIL_RE_.match(value):
        return value
    raise ValueError("The parameter {} is not valid email address".format(name))


# Request parser for cluster POST and PUT requests
cluster_reqparser = reqparse.RequestParser()

cluster_reqparser.add_argument("name", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("description", type=str, location="form",
                               required=True)

cluster_reqparser.add_argument("hostname_ldap_cluster", type=str,
                               location="form", required=True)
cluster_reqparser.add_argument("hostname_oxauth_cluster", type=str,
                               location="form", required=True)
cluster_reqparser.add_argument("hostname_oxtrust_cluster", type=str,
                               location="form", required=True)

cluster_reqparser.add_argument("orgName", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("orgShortName", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("countryCode", type=country_code,
                               location="form", required=True)
cluster_reqparser.add_argument("city", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("state", type=str, location="form",
                               required=True)
cluster_reqparser.add_argument("admin_email", type=admin_email,
                               location="form", required=True)
cluster_reqparser.add_argument("admin_pw", type=str, location="form",
                               required=True)
