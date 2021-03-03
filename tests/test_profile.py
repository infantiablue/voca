def test_profile_dashboard(client):
    response = client.get('/dashboard')
    assert response.status_code == 200


def test_profile_add(client):
    response = client.get('/add')
    assert response.status_code == 200


def test_profile_edit(client):
    response = client.get('/edit')
    assert response.status_code == 200


def test_profile_account(client):
    response = client.get('/account')
    assert response.status_code == 200
