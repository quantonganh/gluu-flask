def test_register_minion(monkeypatch):
    from api.helper.salt_helper import SaltHelper

    # stub unaccepted minion keys
    monkeypatch.setattr(
        "salt.key.Key.list_keys",
        lambda cls: {"minions_pre": ["abc"]},
    )

    # make sure minion key is accepted by checking whether
    # return value is not an empty ``dict``
    assert SaltHelper().register_minion("abc") != {}


def test_unregister_minion(monkeypatch):
    from api.helper.salt_helper import SaltHelper

    # stub accepted minion keys
    monkeypatch.setattr(
        "salt.key.Key.list_keys",
        lambda cls: {"minions": ["abc"]},
    )

    # make sure minion key is deleted by checking whether
    # return value is not an empty ``dict``
    assert SaltHelper().unregister_minion("abc") != {}


def test_is_minion_registered(monkeypatch):
    from api.helper.salt_helper import SaltHelper

    # stub accepted minion keys
    monkeypatch.setattr(
        "salt.key.Key.list_keys",
        lambda cls: {"minions": ["abc"]},
    )

    # make sure minion key is already accepted
    assert SaltHelper().is_minion_registered("abc") is True
