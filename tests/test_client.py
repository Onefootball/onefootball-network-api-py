"""API client tests"""
from onefootball_network.client import OneFootballNetwork


def test_authentication() -> None:
    of = OneFootballNetwork()
    assert "Authorization" in of.session.headers.keys()

    token = of.session.headers["Authorization"].split("Bearer ")[1]
    assert len(token) > 0
