from app import create_app
app = create_app()
client = app.test_client()


def test_profile_dashboard():
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data


def test_profile_add():
    response = client.get('/add')
    assert response.status_code == 200
    assert b'Add word' in response.data


def test_profile_edit():
    response = client.get('/edit')
    assert response.status_code == 200
    assert b'Edit' in response.data


def test_profile_account():
    response = client.get('/account')
    assert response.status_code == 200
    assert b'Account' in response.data
