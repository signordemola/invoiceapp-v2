import random
import pytest

def test_login_route_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_login_with_nonexistent_user(client):
    response = client.post("/login", data={
        "usr_name": "nonexistentuser",
        "psd_wrd": "somepassword"
    })
    assert response.status_code == 200
    assert b"Username does not exist!" in response.data


def test_login_with_wrong_password(client, db_session, test_user):
    username = f'test_user_{random.randrange(1000)}'
    password = "correctpassword"

    test_user(username, password, db_session)

    response = client.post("/login", data={
        "usr_name": username,
        "psd_wrd": "wrongpassword"
    })
    assert response.status_code == 200
    assert "Incorrect Password!" in response.text


def test_successful_login(client, db_session, test_user):
    username = f'test_user_{random.randrange(10)}'
    password = f'pass_{random.randrange(10000)}'

    test_user(username, password, db_session)

    response = client.post("/login", data={
        "usr_name": username,
        "psd_wrd": password
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == "/invoice/"


def test_login_sets_session(client, db_session, test_user):
    username = f'test_user_{random.randrange(1000)}'
    password = "testpassword"

    user = test_user(username, password, db_session)

    with client.session_transaction() as sess:
        assert 'user_id' not in sess

    response = client.post("/login", data={
        "usr_name": username,
        "psd_wrd": password
    })

    with client.session_transaction() as sess:
        assert 'user_id' in sess
        assert sess['user_id'] == user.id


def test_logout(client, authenticated_user):
    user, login_response = authenticated_user()
    assert login_response.status_code == 200

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

    assert response.request.path == "/login"


def test_login_form_validation(client):
    response = client.post("/login", data={
        "usr_name": "",
        "psd_wrd": ""
    })
    assert response.status_code == 200


@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
    ("user3", "pass3"),
])

def test_multiple_users_login(client, db_session, test_user, username, password):
    test_user(username, password, db_session)

    response = client.post("/login", data={
        "usr_name": username,
        "psd_wrd": password
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == "/invoice/"


def test_database_user_creation(db_session, test_user):
    from applib.model import Users

    username = f'test_db_user_{random.randrange(1000)}'
    password = "testpassword"

    created_user = test_user(username, password, db_session)
    db_user = db_session.query(Users).filter(Users.username == username).first()
    assert db_user is not None
    assert db_user.username == username
    assert db_user.password == password
    assert db_user.id == created_user.id