import pytest

from app import connexion


@pytest.fixture
def connexion(user):
    rv = user.post(
        "/connexion", data=dict(username='julien', password='password'), follow_redirects=True
    )
    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find("Login User") == -1