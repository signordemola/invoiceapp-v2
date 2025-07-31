import datetime
import random

def test_create_client_get(client, authenticated_user):
    authenticated_user()

    response = client.get('/client/add')
    assert response.status_code == 200
    assert b"name" in response.data.lower()
    assert b"address" in response.data.lower()
    assert b"phone" in response.data.lower()
    assert b"email" in response.data.lower()


def test_create_client_post_valid(client, db_session, authenticated_user):
    authenticated_user()

    client_data = {
        'name': f'Test Client {random.randrange(1000)}',
        'email': "test@example.com",
        'address': '10, address street, city, state',
        'phone': '09024153146',
        'post_addr': 'P.O Box 34253'
    }

    response = client.post('/client/add', data=client_data, follow_redirects=True)
    assert response.status_code == 200
    print(f'\nValid redirect path: {response.request.path}')
    assert response.request.path == '/invoice/add' in response.request.path

    from applib.model import Client
    with db_session as db:
        created_client = db.query(Client).filter(Client.name == client_data['name']).first()
        print('\n\n\n\n\n\n')
        print(f'Created client: ', created_client)
        assert created_client is not None
        assert created_client.name == client_data['name']
        assert created_client.address == client_data['address']
        assert created_client.phone == client_data['phone']
        assert created_client.email == client_data['email']
        assert created_client.post_addr == client_data['post_addr']
        assert created_client.date_created is not None


def test_create_client_post_invalid(client, authenticated_user):
    authenticated_user()

    invalid_data = {
        'name': f'Test Client {random.randrange(1000)}',
        'email': "invalid-email",
        'address': '10, address street, city, state',
        'phone': '09024153146',
        'post_addr': 'P.O Box 34253'
    }

    response = client.post('/client/add', data=invalid_data, follow_redirects=True)
    print(f'\nInvalid form response status: {response.status_code}')
    print(f'\nInvalid redirect path: {response.request.path}')
    assert response.status_code == 200
    assert response.request.path == '/client/add' in response.request.path


def test_edit_client_get(client, db_session, authenticated_user):
    authenticated_user()

    from applib.model import Client
    test_client_data = Client(
        name=f'Edit Test Client {random.randrange(1000)}',
        address='123 Edit Street',
        phone='555-0456',
        email='edit@example.com',
        post_addr='123 Edit Post Street',
        date_created=datetime.datetime.now()
    )

    with db_session as db:
        db.add(test_client_data)
        db.commit()
        client_id = test_client_data.id

    response = client.get(f'/client/edit/{client_id}')
    assert response.status_code == 200

    assert test_client_data.name.encode() in response.data
    assert test_client_data.address.encode() in response.data
    assert test_client_data.phone.encode() in response.data
    assert test_client_data.email.encode() in response.data


def test_edit_client_post_valid(client, db_session, authenticated_user):
    authenticated_user()

    from applib.model import Client
    test_client_data = Client(
        name=f'Original Client {random.randrange(10)}',
        email='email@example.com',
        address='10, address street, city, state',
        phone='9024153146',
        post_addr='P.O Box 34253',
        date_created=datetime.datetime.now()
    )

    with db_session as db:
        db.add(test_client_data)
        db.commit()
        client_id = test_client_data.id

    updated_data = {
        'name': f'Updated Client {random.randrange(1000)}',
        'email': 'updated@example.com',
        'address': '20, new address street',
        'phone': '0902392343',
        'post_addr': 'No P.O Box Address'
    }

    response = client.post(f'/client/edit/{client_id}',data=updated_data, follow_redirects=True)
    assert response.status_code == 200

    assert response.request.path == '/client/'

    with db_session as db:
        updated_client = db.get(Client, client_id)
        print('\n\n\n', f'Updated client: ', updated_client)
        assert updated_client.name == updated_data['name']
        assert updated_client.address == updated_data['address']
        assert updated_client.phone == updated_data['phone']
        assert updated_client.email == updated_data['email']
        assert updated_client.post_addr == updated_data['post_addr']


def test_edit_client_post_invalid(client, db_session, authenticated_user):
    authenticated_user()

    from applib.model import Client
    test_client_data = Client(
        name=f'Test Client {random.randrange(1000)}',
        address='Test Address',
        phone='555-0000',
        email='test@example.com',
        post_addr='Test Post Address',
        date_created=datetime.datetime.now()
    )

    with db_session as db:
        db.add(test_client_data)
        db.commit()
        client_id = test_client_data.id

    response = client.post(f'/client/edit/{client_id}', data={
        'name': '',
        'address': '',
        'phone': '',
        'email': 'invalid-email',
        'post_addr': ''
    })

    assert response.status_code == 200


def test_edit_nonexistent_client(client, authenticated_user):
    authenticated_user()

    response = client.get('/client/edit/99999')
    assert response.status_code in [404, 500]


def test_client_list_get(client, db_session, authenticated_user):
    authenticated_user()

    from applib.model import Client
    test_clients = []
    for i in range(3):
        test_client = Client(
            name=f'List Test Client {i}_{random.randrange(1000)}',
            address=f'Address {i}',
            phone=f'555-000{i}',
            email=f'client{i}@example.com',
            post_addr=f'Post Address {i}',
            date_created=datetime.datetime.now()
        )
        test_clients.append(test_client)

    with db_session as db:
        db.add_all(test_clients)
        db.commit()

        response = client.get('/client/')
        assert response.status_code == 200

        for test_client in test_clients:
            assert test_client.name.encode() in response.data
            assert test_client.email.encode() in response.data