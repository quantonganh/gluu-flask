import os

import jsonpickle
import pytest


class _DummyNode(object):
    """Acts as a fake Node until we have a stable Node model.
    """
    def __init__(self, id_, type_):
        self.id = id_
        self.type = type_

    def as_dict(self):
        return self.__dict__


def test_cluster_persist(config, cluster):
    fp = os.path.join(config.DB, "cluster_{}.json".format(cluster.id))

    # ensure file is created
    assert os.path.exists(fp)

    # ensure we save the data
    with open(fp) as file_:
        expected_data = jsonpickle.decode(file_.read())
        assert cluster.as_dict() == expected_data.as_dict()


@pytest.mark.parametrize("node, container", [
    (_DummyNode(id_="1", type_="ldap"), "ldap_nodes"),
    (_DummyNode(id_="2", type_="oxauth"), "oxauth_nodes"),
    (_DummyNode(id_="3", type_="oxtrust"), "oxtrust_nodes"),
])
def test_cluster_add_node(cluster, node, container):
    retval = cluster.add_node(node)

    # ensure node is returned as return value
    assert retval == node

    # ensure node added to cluster
    assert getattr(cluster, container)[node.id] == node.as_dict()


def test_cluster_add_unsupported_node(cluster):
    with pytest.raises(ValueError):
        node = _DummyNode(id_="123", type_="random")
        cluster.add_node(node)

        # ensure unsupported node isn't added to cluster
        assert cluster.ldap_nodes == {}
