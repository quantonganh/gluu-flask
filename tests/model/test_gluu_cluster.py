import pytest


class _DummyNode(object):
    """Acts as a fake Node until we have a stable Node model.
    """
    def __init__(self, id_, type_):
        self.id = id_
        self.type = type_

    def as_dict(self):
        return self.__dict__


def test_cluster_add_ldap_node(cluster, ldap_node):
    cluster.add_node(ldap_node)
    assert getattr(cluster, "ldap_nodes")[0] == ldap_node.id


def test_cluster_add_oxauth_node(cluster, oxauth_node):
    cluster.add_node(oxauth_node)
    assert getattr(cluster, "oxauth_nodes")[0] == oxauth_node.id


def test_cluster_add_oxtrust_node(cluster, oxtrust_node):
    cluster.add_node(oxtrust_node)
    assert getattr(cluster, "oxtrust_nodes")[0] == oxtrust_node.id


def test_cluster_add_unsupported_node():
    from api.model import GluuCluster

    cluster = GluuCluster()

    # ensure adding unsupported node raises error
    with pytest.raises(ValueError):
        node = _DummyNode(id_="123", type_="random")
        cluster.add_node(node)


def test_cluster_as_dict():
    from api.model import GluuCluster

    cluster = GluuCluster()
    actual = cluster.as_dict()

    for field in cluster.resource_fields.keys():
        assert field in actual


def test_cluster_remove_ldap_node(cluster, ldap_node):
    cluster.add_node(ldap_node)
    cluster.remove_node(ldap_node)
    assert getattr(cluster, "ldap_nodes") == []


def test_cluster_remove_oxauth_node(cluster, oxauth_node):
    cluster.add_node(oxauth_node)
    cluster.remove_node(oxauth_node)
    assert getattr(cluster, "oxauth_nodes") == []


def test_cluster_remove_oxtrust_node(cluster, oxtrust_node):
    cluster.add_node(oxtrust_node)
    cluster.remove_node(oxtrust_node)
    assert getattr(cluster, "oxtrust_nodes") == []


def test_cluster_remove_unsupported_node():
    from api.model import GluuCluster

    cluster = GluuCluster()

    # ensure removing unsupported node raises error
    with pytest.raises(ValueError):
        node = _DummyNode(id_="123", type_="random")
        cluster.remove_node(node)


def test_cluster_update_fields(db, cluster):
    data = {"name": "hello"}
    cluster.set_fields(data)
    assert cluster.name == "hello"
