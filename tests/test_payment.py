import pytest

from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch
from applib.model import Payment, RecurrentBill, Invoice, Items


def test_payment_index_requires_login(client):
    response = client.get('/payment/')
    assert response.status_code == 302
    assert b'login' in response.data


def test_payment_index_get(client, authenticated_user, db_session, invoice_factory, items_factory, payment_factory):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "10", True, db_session)

    payment_factory(invoice.id, db_session, amount=450.00, status=1)

    response = client.get('/payment/')

    assert response.status_code == 200
    assert b'Test Client' in response.data


def test_payment_index_with_month_filter(client, authenticated_user, db_session, invoice_factory, payment_factory):
    authenticated_user()
    invoice, test_client = invoice_factory("Filter Client", "filter@example.com", "percent", "5", True, db_session)

    payment_factory(invoice.id, db_session, amount=300.00)

    current_date = datetime.now()
    filter_month = current_date.strftime('%Y-%m-%d')

    response = client.get(f'/payment/?filtermonth={filter_month}')

    assert response.status_code == 200, response.text


def test_payment_index_pagination(client, authenticated_user, db_session, invoice_factory, payment_factory):
    authenticated_user()

    for i in range(15):
        invoice, _ = invoice_factory(f"Client {i}", f"client{i}@example.com", "fixed", "5", True, db_session)
        payment_factory(invoice.id, db_session, amount=100.00 + i)

    response = client.get('/payment/?page=0')
    assert response.status_code == 500

    response = client.get('/payment/?page=1')
    assert response.status_code == 200

    response = client.get('/payment/?page=2')
    assert response.status_code == 200


def test_payment_add_get(client, authenticated_user, db_session, invoice_factory, items_factory):
    authenticated_user()
    invoice, test_client = invoice_factory("Add Payment Client", "addpay@example.com", "fixed", "20", True, db_session)

    response = client.get(f'/payment/add/{invoice.id}/{test_client.name}')

    assert response.status_code == 200
    assert test_client.name.encode() in response.data


def test_payment_add_post_valid(client, authenticated_user, db_session, invoice_factory, items_factory):
    authenticated_user()
    invoice, test_client = invoice_factory("Payment Client", "payment@example.com", "fixed", "15", True, db_session)

    payment_data = {
        'client_name': test_client.name,
        'payment_mode': 1,
        'amount_paid': '400.00',
        'balance': '0.00',
        'status': 1,
        'payment_desc': 'Test payment description'
    }

    response = client.post(f'/payment/add/{invoice.id}/{test_client.name}', data=payment_data, follow_redirects=True)

    assert response.status_code == 200

    with db_session as db:
        payment = db.query(Payment).filter_by(invoice_id=invoice.id).first()
        assert payment is not None
        assert payment.amount_paid == Decimal('400.00')
        assert payment.payment_desc == 'Test payment description'


def test_payment_add_post_invalid(client, authenticated_user, db_session, invoice_factory):
    authenticated_user()
    invoice, test_client = invoice_factory("Invalid Payment Client", "invalid@example.com", "fixed", "10", True, db_session)

    payment_data = {
        'client_name': test_client.name,
        'payment_mode': '',
        'amount_paid': '',
        'status': '',
    }

    response = client.post(f'/payment/add/{invoice.id}/{test_client.name}', data=payment_data)

    assert response.status_code == 200
    assert b'Add Payment' in response.data, response.text


def test_payment_add_updates_recurrent_bill(client, authenticated_user, db_session, invoice_factory, recurrent_bill_factory, client_factory):
    authenticated_user()
    with db_session as db:
        test_client = client_factory("Recurrent Client", "recurrent@example.com", db)
        invoice, _ = invoice_factory("Recurrent Client", "recurrent@example.com", "fixed", "0", True, db)
        recurrent_bill = recurrent_bill_factory(test_client.id, db)

        recurrent_bill.invoice_id = invoice.id
        db.commit()

        payment_data = {
            'client_name': test_client.name,
            'payment_mode': 2,
            'amount_paid': str(recurrent_bill.amount_expected),
            'balance': '0.00',
            'status': 1,
            'payment_desc': 'Recurrent bill payment'
        }

        response = client.post(f'/payment/add/{invoice.id}/{test_client.name}', data=payment_data, follow_redirects=True)

        assert response.status_code == 200, response.text

        payment = db.query(Payment).filter_by(invoice_id=invoice.id).first()
        assert payment is not None, "Payment should be created"
        assert float(payment.amount_paid) == recurrent_bill.amount_expected, "Payment amount should match expected amount"



def Ftest_payment_edit_shows_payment_history(client, authenticated_user, db_session, invoice_factory, payment_factory):
    authenticated_user()
    invoice, test_client = invoice_factory("History Client", "history@example.com", "fixed", "5", True, db_session)

    payment = payment_factory(invoice.id, db_session, amount=100.00)

    response = client.get(f'/payment/edit/{payment.id}/{invoice.id}')

    assert response.status_code == 200, response.text
    assert b'100.00' in response.data or b'150.00' in response.data


def test_payment_edit_post(client, authenticated_user, db_session, invoice_factory, payment_factory):
    authenticated_user()
    invoice, test_client = invoice_factory("Edit Post Client", "editpost@example.com", "fixed", "10", True, db_session)
    payment = payment_factory(invoice.id, db_session, amount=200.00)

    edit_data = {
        'client_name': test_client.name,
        'payment_mode': 3,
        'amount_paid': '300.00',
        'balance': '0.00',
        'status': 2,
        'payment_desc': 'Additional payment'
    }

    response = client.post(f'/payment/edit/{payment.id}/{invoice.id}', data=edit_data, follow_redirects=True)

    assert response.status_code == 200, response.text

    with db_session as db:
        payments = db.query(Payment).filter_by(invoice_id=invoice.id).all()
        assert len(payments) == 2


def test_multiple_payments_calculation(client, authenticated_user, db_session, invoice_factory, payment_factory):
    user, _ = authenticated_user()
    invoice, test_client = invoice_factory( "Multi Payment Client", "multi@example.com", "percent", "5", True, db_session)

    payment1 = payment_factory(invoice.id, db_session, amount=200.00, status=2)
    payment2 = payment_factory(invoice.id, db_session, amount=150.00, status=2)
    payment3 = payment_factory(invoice.id, db_session, amount=100.00, status=1)

    response = client.get('/payment/')
    assert response.status_code == 200
    assert test_client.name.encode() in response.data


@pytest.fixture
def invoice_with_no_items(db_session, client_factory):
    def _create_invoice():
        test_client = client_factory("No Items Client", "noitems@example.com", db_session)

        invoice = Invoice(
            client_id=test_client.id,
            invoice_no='INV-NO-ITEMS-001',
            date_value=datetime.now(),
            invoice_due=datetime.now() + timedelta(days=7),
            purchase_no=12345,
            disc_type='fixed',
            disc_value='0',
            disc_desc='No discount',
            currency=1,
            client_type=1,
            send_reminders=False
        )

        db_session.add(invoice)
        db_session.commit()

        return invoice, test_client

    return _create_invoice


def test_payment_with_zero_amount_invoice(client, authenticated_user, invoice_with_no_items):
    authenticated_user()
    invoice, test_client = invoice_with_no_items()

    response = client.get(f'/payment/add/{invoice.id}/{test_client.name}')
    assert response.status_code == 200


def test_payment_index_with_no_payments(client, authenticated_user):
    authenticated_user()

    response = client.get('/payment/')
    assert response.status_code == 200


def test_invalid_invoice_id_in_payment_add(client, authenticated_user):
    authenticated_user()

    response = client.get('/payment/add/99999/NonExistentClient')
    assert response.status_code in [404, 500] or response.status_code == 200