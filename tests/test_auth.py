def test_auth_register(client):
    response = client.get('/register')
    assert response.status_code == 200


def test_auth_login(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_auth_logout(client):
    response = client.get('/logout')
    assert response.status_code == 200
