def test_user_model(db_session):
    from applib.model import Users

    user = Users(username="test_user", password="hashed_pwd")
    db_session.add(user)
    db_session.commit()

    queried_user = db_session.query(Users).filter_by(username="test_user").first()
    assert queried_user is not None
    assert queried_user.username == "test_user"


def test_client_model(db_session):
    from applib.model import Client
    client = Client(name="Test Client", email="test@example.com",address='10, address street, city, state', phone='09024153146', post_addr='P.O Box 34253', date_created='2025-03-03')
    db_session.add(client)
    db_session.commit()
    assert db_session.query(Client).count() == 1