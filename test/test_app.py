import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app({"TEST": True})
    clear_all()
    with app.test_client() as client:
        yield client


def _create_user(client, name, email, password):
    rv = client.post(
        "/register",
        data=dict(name=name, email=email, password=password),
        follow_redirects=True,
    )
    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find("Inscrit") == -1


def _login_user(client, email, password):
    rv = client.post(
        "/login", data=dict(email=email, password=password), follow_redirects=True
    )
    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find("Connecté") == -1


def _logout_user(client):
    rv = client.get("/logout", follow_redirects=True)
    assert rv.status_code == 200