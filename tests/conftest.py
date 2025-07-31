import random
from contextlib import contextmanager

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from applib.lib.helper import set_db_uri
from applib.model import Base
from serve import create_app

con_str = set_db_uri()
TEST_ENGINE = create_engine(con_str, echo=False, pool_size=100)


@pytest.fixture(scope='session')
def setup_database():
    Base.metadata.create_all(TEST_ENGINE)
    yield


@contextmanager
def sql_cursor():
    Cursor = sessionmaker(TEST_ENGINE)
    session = Cursor()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@pytest.fixture(scope='function')
def db_session():
    Cursor = sessionmaker(TEST_ENGINE)
    session = Cursor()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@pytest.fixture(scope='module')
def app(setup_database):
    app = create_app()

    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': con_str,
        'SERVER_NAME': 'localhost',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
    })

    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_user():
    def create_test_user(username, password, db_session, hash_password=False):
        from applib.model import Users

        if hash_password:
            password = generate_password_hash(password)

        user = Users(username=username, password=password)
        db_session.add(user)
        db_session.commit()
        return user

    return create_test_user


@pytest.fixture
def authenticated_user(client, db_session, test_user):
    def login_as_user(username=None, password=None):
        if username is None:
            username = f'testuser-{random.randrange(10)}'
        if password is None:
            password = f'testpass-{random.randrange(1000)}'

        user = test_user(username, password, db_session)

        response = client.post('/login', data={
            'usr_name': username,
            'psd_wrd': password
        }, follow_redirects=True)

        print('\n\n', f'User {username} is logged in!')
        return user, response

    return login_as_user


@pytest.fixture
def client_factory():
    def create_test_client(client_name, client_email, db_session):
        from applib.model import Client
        from datetime import datetime

        test_client = Client(
            name=client_name,
            address='123 Test Street',
            phone='0902392343',
            email=client_email,
            post_addr='123 Post Street',
            date_created=datetime.now()
        )

        db_session.add(test_client)
        db_session.commit()

        return test_client

    return create_test_client



@pytest.fixture
def invoice_factory():
    def create_test_invoice(client_name, client_email, disc_type, disc_value, with_items, db_session):
        from applib.model import Client, Invoice, Items
        from datetime import datetime, timedelta

        test_client = Client(
            name=client_name,
            address='123 Invoice Street',
            phone='0902392343',
            email=client_email,
            post_addr='123 Invoice Street',
            date_created=datetime.now()
        )

        db_session.add(test_client)
        db_session.flush()

        test_invoice = Invoice(
            client_id=test_client.id,
            invoice_no=f'INV-TEST-{random.randrange(10000)}',
            date_value=datetime.now(),
            invoice_due=datetime.now() + timedelta(days=7),
            purchase_no=random.randrange(1000),
            disc_type=disc_type,
            disc_value=disc_value,
            disc_desc='Test discount',
            currency=1,
            client_type=1,
            send_reminders=False
        )

        db_session.add(test_invoice)
        db_session.flush()

        if with_items:
            test_item = Items(
                invoice_id=test_invoice.id,
                item_desc='Test Item',
                qty=2,
                rate=100.00,
                amount=500.00
            )
            db_session.add(test_item)

        db_session.commit()
        return test_invoice, test_client

    return create_test_invoice


@pytest.fixture
def items_factory():
    def create_test_items(invoice_id, db_session, num_items=1):
        from applib.model import Items

        items = []
        for i in range(num_items):
            item = Items(
                invoice_id=invoice_id,
                item_desc=f'Test Item {i + 1}',
                qty=random.randint(1, 5),
                rate=random.randint(100, 1000),
                amount=random.randint(100, 5000)
            )
            db_session.add(item)
            items.append(item)

        db_session.commit()
        return items if num_items > 1 else items[0]

    return create_test_items


@pytest.fixture
def payment_factory():
    def create_test_payment(invoice_id, db_session, amount=500.00, status=1):
        from applib.model import Payment
        from datetime import datetime

        payment = Payment(
            client_name='Test Client',
            payment_desc='Test payment',
            date_created=datetime.now(),
            payment_mode=1,
            amount_paid=amount,
            balance=0.00,
            invoice_id=invoice_id,
            status=status
        )

        db_session.add(payment)
        db_session.commit()
        return payment

    return create_test_payment


@pytest.fixture
def recurrent_bill_factory():
    def create_test_recurrent_bill(client_id, db_session):
        from applib.model import RecurrentBill
        from datetime import datetime, timedelta

        bill = RecurrentBill(
            client_id=client_id,
            product_name='Monthly Subscription',
            amount_expected=299.99,
            date_created=datetime.now(),
            date_due=datetime.now() + timedelta(days=30),
            date_updated=datetime.now(),
            payment_status=0
        )

        db_session.add(bill)
        db_session.commit()
        return bill

    return create_test_recurrent_bill



@pytest.fixture(autouse=True)
def cleanup_users():
    yield

    with sql_cursor() as db:
        db.execute(text("""
            TRUNCATE TABLE 
                payment, item, email_queue, email_receipt_count, 
                expense, invoice, recurrent_bill, client, users 
            RESTART IDENTITY CASCADE
        """))
        db.commit()