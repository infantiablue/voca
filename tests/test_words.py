import os
from flask_login import current_user


def test_words_browse(client, auth):
    auth.login()
    response = client.get('/words/browse')
    assert response.status_code == 200
    assert b'ace' in response.data


def test_words_browse_with_pagination(client, auth):
    auth.login()
    response = client.get('/words/browse/page/2')
    assert response.status_code == 200
    assert b'exacerbate' in response.data


def test_sense(client, auth):
    auth.login()
    response = client.get('/sense')
    assert response.status_code == 404

    response = client.get('/sense/abc123')
    assert response.status_code == 404

    response = client.get('/sense/ace')
    assert response.status_code == 200

    response = client.get('/sense/apple')
    assert response.status_code == 404


def test_api_call_from_service(client, auth):
    auth.login()
    response = client.get('/api/lookup/apple')
    assert response.status_code == 200
    # Test if cache worked
    assert os.path.exists(f'{os.getcwd()}/cache/apple.json')


def test_api_call_false_from_service(client, auth):
    auth.login()
    response = client.get('/api/lookup/zteuiyw')
    assert response.status_code == 404
    assert not os.path.exists(f'{os.getcwd()}/cache/zteuiyw.json')


def test_api_call_from_cache(client, auth):
    auth.login()
    response = client.get('/api/lookup/ace')
    assert response.status_code == 200


def test_add_word(app, client, auth):
    auth.login()
    response = client.get('/word/add')
    assert response.status_code == 200
    with client:
        response = client.post(
            '/word/add', data={'word': 'apple'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'A new word has been added.' in response.data
        with app.app_context():
            word = current_user.words.filter_by(text='apple').first()
            assert word is not None
    os.remove(f'{os.getcwd()}/cache/apple.json')


def test_add_without_cache_word(app, client, auth):
    auth.login()
    response = client.get('/word/add')
    assert response.status_code == 200
    with client:
        response = client.post(
            '/word/add', data={'word': 'banana'})
        assert response.status_code == 302
        # assert b'The word has not been defined.' in response.data
        with app.app_context():
            word = current_user.words.filter_by(text='banana').first()
            assert word is None


def test_add_duplicated_word(client, auth):
    auth.login()
    with client:
        response = client.post(
            '/word/add', data={'word': 'ace'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'This word is duplicated.' in response.data


def test_add_nomeaning_word(client, auth):
    auth.login()
    with client:
        response = client.post(
            '/word/add', data={'word': 'awerwerce'}, follow_redirects=True)
        assert b'The word has not been defined.' in response.data


def test_add_note(client, auth):
    auth.login()
    response = client.get('/edit')
    assert response.status_code == 404

    response = client.get('/edit/ace')
    assert response.status_code == 200

    response = client.post(
        '/edit/ace', data={'note': 'example'}, follow_redirects=True)
    assert b'Updated note successfully.' in response.data
    response = client.get('/sense/ace')
    assert b'example' in response.data


def test_remove_word(app, client, auth):
    auth.login()
    with client:
        response = client.post('/word/remove', data={'word': 'ace'})
        assert b'success' in response.data
        with app.app_context():
            word = current_user.words.filter_by(text='ace').first()
            assert word is None
