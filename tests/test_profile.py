import pytest


def test_profile_dashboard(client, auth):
    auth.login()
    with client:
        response = client.get('/dashboard')
        assert b'Recently' in response.data


def test_profile_account(client, auth):
    auth.login()
    with client:
        response = client.get('/account')
        assert b'Update Password' in response.data


@pytest.mark.parametrize(('current_password', 'new_password', 'confirmation', 'message'), (
    ('1234', 'abcd', '12345', b'Passwords must match.'),
    ('12345', 'abcd', 'abcd', b'Incorrect current password.'),
    ('1234', 'abc', 'abc', b'Field must be between 4 and 25 characters long.'),
))
def test_change_password_with_invalidate_input(client, auth, current_password, new_password, confirmation, message):
    response = auth.login()
    with client:
        response = client.post(
            '/account', data={'current_password': current_password, 'new_password': new_password, 'confirmation': confirmation},
            follow_redirects=True
        )
        assert message in response.data


@pytest.mark.parametrize(('current_password', 'new_password', 'confirmation', 'message'), (
    ('1234', 'abcd', 'abcd', b'Changed password successfully.'),
    # ('abcd', '1234', '1234', b'Changed password successfully.'),
))
def test_change_password_with_validate_input(client, auth, current_password, new_password, confirmation, message):
    # print(current_password)
    auth.login(password=current_password)
    with client:
        response = client.post(
            '/account', data={'current_password': current_password, 'new_password': new_password, 'confirmation': confirmation},
            follow_redirects=True
        )
        assert message in response.data
