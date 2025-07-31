def test_user_model(db_session):
    from applib.model import Users
    from werkzeug.security import generate_password_hash

    user = Users(username="testuser", password=generate_password_hash('testpass'))
    db_session.add(user)
    db_session.commit()

    queried_user = db_session.query(Users).first()
    assert queried_user is not None
    assert queried_user.username == "testuser"


def test_client_model(db_session):
    from applib.model import Client
    from datetime import datetime

    client = Client(name="Test Client", email="test@example.com",address='10, address street, city, state', phone='09024153146', post_addr='P.O Box 34253', date_created=datetime.now())
    db_session.add(client)
    db_session.commit()
    assert db_session.query(Client).count() == 1