import pytest
from flask_login import current_user


@pytest.mark.parametrize('path', (
    '/dashboard',
    '/account',
    '/logout',
    '/words/browse',
    '/word/add',
))
def test_login_required(client, path):
    response = client.get(path)
    assert 'http://localhost/login' in response.headers['Location']


def test_register(app, client, auth):
    assert client.get('/join').status_code == 200
    response = client.post(
        '/join', data={'username': 'infantiablue', 'email': 'infantiablue@yahoo.com', 'password': 'abcdef', 'confirmation': 'abcdef'},
        follow_redirects=True
    )
    auth.login(username='infantiablue', password='abcdef')
    from app.models import User
    assert b'Thanks for your registration.' in response.data
    with app.app_context():
        new_user = User.query.filter_by(username='infantiablue').first()
        assert new_user is not None


@pytest.mark.parametrize(('username', 'email', 'password', 'confirmation', 'message'), (
    # ('', '', b'Username is required.'),
    # ('a', '', b'This email address has been registed.'),
    ('a', 'truong.phan@outlook.com', 'b', 'b',
     b'Field must be between 4 and 25 characters long.'),
    ('truongphan', 'a@a', 'b', 'b',
     b'Field must be between 6 and 35 characters long.'),
    ('truongphan', 'truong@gmail.com', 'abcd', 'bcdda',
     b'Passwords must match.'),
    ('truongphan', 'dangtruong@gmail.com', 'abcd', 'abcd',
     b'This email address has been registered.'),
    ('truong', 'truong.phan@outlook.com', 'abcd', 'abcd',
     b'This email address has been registered.'),
    ('dangtruong', 'truong.phan@outlook.com', 'abc', 'abc',
     b'Field must be between 4 and 25 characters long.'),
))
def test_register_validate_input(client, username, email, password, confirmation, message):
    response = client.post(
        '/join',
        data={'username': username, 'email': email,
              'password': password, 'confirmation': confirmation}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/login').status_code == 200
    response = auth.login()
    with client:
        client.get('/')
        assert response.status_code == 200
        assert current_user.username == 'truong'
        assert b'Recently' in response.data


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('abcd', 'test', b'Username is not existed.'),
    ('truong', 'abcd', b'Incorrect Password.'),
))
def test_login_with_invalidate_input(client, auth, username, password, message):
    assert client.get('/login').status_code == 200
    response = auth.login(username, password)
    assert message in response.data


def test_auth_logout(client, auth):
    # response = client.get('/logout')
    response = auth.logout()
    assert response.status_code == 200
    assert not current_user
    assert b'Log In' in response.data
