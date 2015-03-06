def test_register_minion(monkeypatch):
    from api.helper.salt_helper import register_minion

    # stub unaccepted minion keys
    monkeypatch.setattr(
        "salt.key.Key.list_keys",
        lambda cls: {"minions_pre": ["abc"]},
    )

    # make sure minion key is accepted by checking whether
    # return value is not an empty ``dict``
    assert register_minion("abc") != {}


def test_unregister_minion(monkeypatch):
    from api.helper.salt_helper import unregister_minion

    # stub accepted minion keys
    monkeypatch.setattr(
        "salt.key.Key.list_keys",
        lambda cls: {"minions": ["abc"]},
    )

    # make sure minion key is deleted by checking whether
    # return value is not an empty ``dict``
    assert unregister_minion("abc") != {}
