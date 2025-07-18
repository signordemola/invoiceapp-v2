from flask import url_for

from applib.model import Users

def test_login_route(client, db_session):
    user = Users(username="testuser", password='testpass')
    db_session.add(user)
    db_session.commit()

    response = client.post("/login", data={
        "usr_name": "testuser",
        "psd_wrd": "testpass"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == url_for('invoice.index')

    print(f"Status Code: {response.status_code}")
    print(f"Response Data: {response.data.decode()}")

    response = client.post("/login", data={
        "usr_name": "testusersss",
        "psd_wrd": "testpass"
    })
    assert b"Username does not exist!" in response.data

    response = client.post("/login", data={
        "usr_name": "testuser",
        "psd_wrd": "wrongpass"
    })
    assert b"Incorrect Password!" in response.data