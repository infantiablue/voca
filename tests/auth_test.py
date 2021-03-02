from app import create_app
app = create_app()
client = app.test_client()


def test_auth_register():
    response = client.get('/register')
    assert response.status_code == 200


def test_auth_login():
    response = client.get('/login')
    assert response.status_code == 200


def test_auth_logout():
    response = client.get('/logout')
    assert response.status_code == 200
