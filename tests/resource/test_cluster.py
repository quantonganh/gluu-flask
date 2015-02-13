def test_cluster_post(app):
    resp = app.test_client().post("/cluster")
    assert resp.status_code == 200
    assert "echo" in resp.data
