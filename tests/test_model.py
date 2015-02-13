import uuid


def test_cluster_persist(config):
    import os
    import jsonpickle
    from api.model import GluuCluster

    cluster = GluuCluster()
    cluster.id = "{}".format(uuid.uuid4())
    json_data = cluster.persist(config.DB)

    fp = os.path.join(config.DB, "cluster_{}.json".format(cluster.id))

    # ensure file is created
    assert os.path.exists(fp)

    # ensure we save the data
    with open(fp) as file_:
        expected_json = jsonpickle.decode(file_.read())
        assert json_data == expected_json

    # remove test file
    os.unlink(fp)
