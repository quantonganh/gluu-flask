# import jsonpickle
import pytest


class _DummyNode(object):
    """Acts as a fake Node until we have a stable Node model.
    """
    def __init__(self, id_, type_):
        self.id = id_
        self.type = type_

    def as_dict(self):
        return self.__dict__


@pytest.mark.parametrize("node, container", [
    (_DummyNode(id_="1", type_="gluuopendj"), "ldap_nodes"),
    (_DummyNode(id_="2", type_="oxauth"), "oxauth_nodes"),
    (_DummyNode(id_="3", type_="oxtrust"), "oxtrust_nodes"),
])
def test_cluster_add_node(cluster, node, container):
    cluster.add_node(node)
    # ensure node added to cluster
    assert getattr(cluster, container)[0] == node.id


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


@pytest.mark.parametrize("node, container", [
    (_DummyNode(id_="1", type_="gluuopendj"), "ldap_nodes"),
    (_DummyNode(id_="2", type_="oxauth"), "oxauth_nodes"),
    (_DummyNode(id_="3", type_="oxtrust"), "oxtrust_nodes"),
])
def test_cluster_remove_node(cluster, node, container):
    cluster.add_node(node)
    cluster.remove_node(node)

    # ensure node removed from cluster
    assert getattr(cluster, container) == []


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
