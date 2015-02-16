import os
import uuid
import jsonpickle


def test_cluster_persist(config):
    from api.model import GluuCluster

    cluster = GluuCluster()
    cluster.id = "{}".format(uuid.uuid4())
    obj = cluster.persist(config.DB)

    fp = os.path.join(config.DB, "cluster_{}.json".format(cluster.id))

    # ensure file is created
    assert os.path.exists(fp)

    # ensure we save the data
    with open(fp) as file_:
        expected_data = jsonpickle.decode(file_.read())
        assert obj.as_dict() == expected_data.as_dict()

    # remove test file
    os.unlink(fp)
