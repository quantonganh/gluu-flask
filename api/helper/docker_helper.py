from docker import Client
import subprocess
import sys
from time import sleep
from random import randrange


def get_image(name='', docker_base_url='unix://var/run/docker.sock'):
    try:
        c = Client(base_url=docker_base_url)
        return c.images(name)
    except:
        # TODO add logging
        print "Error making connection to Docker Server"
    return None


def build_image(node_type = ''):
    run('mkdir /tmp/{}'.format(node_type))
    raw_url = 'https://raw.githubusercontent.com/GluuFederation/gluu-docker/master/ubuntu/14.04/{}/Dockerfile'.format(node_type)
    run('wget -q {} -P /tmp/{}'.format(raw_url, node_type))
    run('docker build -q --rm --force-rm -t {} {}'.format(node_type, '/tmp/{}'.format(node_type)))
    run('rm -rf /tmp/{}'.format(node_type))


def run(command, exit_on_error=True, cwd=None):
    try:
        return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, cwd=cwd)
    except subprocess.CalledProcessError, e:
        if exit_on_error:
            sys.exit(e.returncode)
        else:
            raise


def run_container(node = None):
    image = get_image(node.type)
    if not image:
        build_image(node.type)
    con_name = '{0}_{1}_{2}'.format(node.type, node.cluster_name, randrange(101, 999))
    cid = run('docker run -d -P --name={0} {1}'.format(con_name, node.type))
    scid = cid.strip()[:-(len(cid) - 12)]
    node.id = scid
    sleep(10)
    run('salt-key -y -a {}'.format(node.scid))


def render_ldap_properties(node = None):
    pass


def run_ldap_setup(node = None):
    pass

