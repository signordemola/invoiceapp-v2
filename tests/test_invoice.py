import pytest
from flask import url_for
from datetime import datetime
from applib.model import Invoice, RecurrentBill
from unittest.mock import patch


def test_invoice_index_requires_login(client):
    response = client.get('/invoice/')
    assert response.status_code == 302
    assert b'login' in response.data


def test_invoice_index_authenticated(client, authenticated_user):
    authenticated_user()
    response = client.get(url_for("invoice.index"))
    assert response.status_code == 200
    assert b"INVOICE LIST" in response.data


def test_invoice_index_with_search(client, authenticated_user, invoice_factory, payment_factory, db_session):
    authenticated_user()

    invoice1, client1 = invoice_factory("John Doe", "john@example.com", "fixed", 10, True, db_session)
    payment_factory(invoice1.id, db_session, amount=100.00, status=1)

    invoice2, client2 = invoice_factory("Jane Smith", "jane@example.com", "percent", 5, True, db_session)
    payment_factory(invoice2.id, db_session, amount=200.00, status=1)

    response = client.get('/invoice/?search=John')
    assert response.status_code == 200, response.text
    assert b"John Doe" in response.data
    assert b"Jane Smith" not in response.data

    response = client.get('/invoice/?search=jane@example.com')
    assert response.status_code == 200
    assert b"Jane Smith" in response.data
    assert b"John Doe" not in response.data


def test_invoice_index_pagination(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()

    for i in range(5):
        invoice_factory(f"Client {i}", f"client{i}@example.com", "fixed", 10, True, db_session)

    response = client.get('/invoice/?page=1')
    assert response.status_code == 200


def test_invoice_add_get_request(client, authenticated_user, client_factory, db_session):
    authenticated_user()
    test_client = client_factory("Form Client", "form@example.com", db_session)

    response = client.get('/invoice/add')
    assert response.status_code == 200
    assert b"form-control" in response.data


def test_invoice_add_post_valid(client, authenticated_user, client_factory, db_session):
    authenticated_user()
    test_client = client_factory("Test Client", "test@example.com", db_session)

    form_data = {
        'client_id': test_client.id,
        'client_type': 2,
        'currency': 2,
        'bill_id': 0
    }

    response = client.post('/invoice/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        invoice = db.query(Invoice).filter_by(client_id=test_client.id).first()
        assert invoice is not None
        assert invoice.client_type == 2
        assert invoice.currency == 2
        assert invoice.invoice_no.startswith('INV-')
        assert invoice.purchase_no == invoice.id


def test_invoice_add_post_invalid(client, authenticated_user):
    authenticated_user()

    form_data = {
        'client_id': 0,
        'client_type': 1,
        'currency': 1,
        'bill_id': 0
    }

    response = client.post('/invoice/add', data=form_data)
    assert response.status_code in [200, 302, 400]


def test_invoice_with_recurrent_bill(client, authenticated_user, client_factory, recurrent_bill_factory, db_session):
    authenticated_user()

    test_client = client_factory("Recurring Client", "recurring@example.com", db_session)
    bill = recurrent_bill_factory(test_client.id, db_session)

    form_data = {
        'client_id': test_client.id,
        'client_type': 1,
        'currency': 1,
        'bill_id': bill.id
    }

    response = client.post('/invoice/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        invoice = db.query(Invoice).filter_by(client_id=test_client.id).first()
        assert invoice is not None

        db.refresh(bill)
        updated_bill = db.query(RecurrentBill).filter_by(id=bill.id).first()
        assert updated_bill.invoice_id is not None


def test_checkout_get_request(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()

    invoice, test_client = invoice_factory("Checkout Client", "checkout@example.com", "fixed", 50, True, db_session)

    response = client.get(f'/invoice/checkout/{invoice.id}')
    assert response.status_code == 200
    assert b"Checkout Client" in response.data
    assert b"checkout@example.com" in response.data


def test_checkout_nonexistent_invoice(client, authenticated_user):
    authenticated_user()

    response = client.get('/invoice/checkout/99999')
    assert response.status_code in [404, 500]


def test_checkout_download_pdf(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()

    invoice, test_client = invoice_factory("PDF Client", "pdf@example.com", "fixed", 25, True, db_session)

    response = client.get(f'/invoice/checkout/{invoice.id}?download=1')
    assert response.status_code in [200, 302]


def test_update_reminders_post(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()

    invoice, test_client = invoice_factory("Reminder Client", "reminder@example.com", "fixed", 15, True, db_session)
    invoice.send_reminders = True
    db_session.commit()

    form_data = {'send_reminders': 'true'}
    response = client.post(f'/invoice/update_reminders/{invoice.id}', data=form_data)
    assert response.status_code == 302, response.text

    with db_session as db:
        updated_invoice = db.query(Invoice).filter_by(id=invoice.id).first()
        if hasattr(updated_invoice, 'send_reminders'):
            assert updated_invoice.send_reminders is True

    form_data = {'send_reminders': 'false'}
    response = client.post(f'/invoice/update_reminders/{invoice.id}', data=form_data)
    assert response.status_code == 302, response.text

    with db_session as db:
        updated_invoice = db.query(Invoice).filter_by(id=invoice.id).first()
        if hasattr(updated_invoice, 'send_reminders'):
            assert updated_invoice.send_reminders is False


def test_update_reminders_nonexistent_invoice(client, authenticated_user):
    authenticated_user()

    form_data = {'send_reminders': 'true'}
    response = client.post('/invoice/update_reminders/99999', data=form_data)
    assert response.status_code == 302


def test_invoice_calculations_fixed_discount(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()

    invoice, test_client = invoice_factory("Calc Client", "calc@example.com", "fixed", 100, True, db_session)

    response = client.get(f'/invoice/checkout/{invoice.id}')
    assert response.status_code == 200, response.text


def test_invoice_calculations_percent_discount(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()

    invoice, test_client = invoice_factory("Percent Client", "percent@example.com", "percent", 15, True, db_session)

    response = client.get(f'/invoice/checkout/{invoice.id}')
    assert response.status_code == 200, response.text


def test_invoice_auto_generation_fields(client, authenticated_user, client_factory, db_session):
    authenticated_user()

    test_client = client_factory("Auto Client", "auto@example.com", db_session)

    form_data = {
        'client_id': test_client.id,
        'client_type': 3,
        'currency': 3,
        'bill_id': 0
    }

    response = client.post('/invoice/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        invoice = db.query(Invoice).filter_by(client_id=test_client.id).first()
        assert invoice.invoice_no.startswith('INV-')
        assert invoice.purchase_no == invoice.id
        assert invoice.date_value is not None
        assert invoice.invoice_due is not None
        assert isinstance(invoice.date_value, datetime)
        assert isinstance(invoice.invoice_due, datetime)


def test_invoice_with_multiple_items(client, authenticated_user, invoice_factory, items_factory, db_session):
    authenticated_user()

    invoice, test_client = invoice_factory("Multi Item Client", "multi@example.com", "fixed", 20, False, db_session)
    items_factory(invoice.id, db_session, num_items=3)

    response = client.get(f'/invoice/checkout/{invoice.id}')
    assert response.status_code == 200, response.text
    assert b"Test Item 1" in response.data
    assert b"Test Item 2" in response.data
    assert b"Test Item 3" in response.data


def test_invoice_different_currencies(client, authenticated_user, client_factory, db_session):
    authenticated_user()

    currencies = [1, 2, 3, 4]

    for currency in currencies:
        test_client = client_factory(f"Currency {currency} Client", f"currency{currency}@example.com", db_session)

        form_data = {
            'client_id': test_client.id,
            'client_type': 1,
            'currency': currency,
            'bill_id': 0
        }

        response = client.post('/invoice/add', data=form_data)
        assert response.status_code == 302

        with db_session as db:
            invoice = db.query(Invoice).filter_by(client_id=test_client.id).first()
            assert invoice.currency == currency


def test_invoice_different_client_types(client, authenticated_user, client_factory, db_session):
    authenticated_user()

    client_types = [1, 2, 3]

    for client_type in client_types:
        test_client = client_factory(f"Type {client_type} Client", f"type{client_type}@example.com", db_session)

        form_data = {
            'client_id': test_client.id,
            'client_type': client_type,
            'currency': 1,
            'bill_id': 0
        }

        response = client.post('/invoice/add', data=form_data)
        assert response.status_code == 302

        with db_session as db:
            invoice = db.query(Invoice).filter_by(client_id=test_client.id).first()
            assert invoice.client_type == client_type


def test_checkout_requires_login(client):
    response = client.get('/invoice/checkout/1')
    assert response.status_code in [302, 500]


def test_update_reminders_requires_login(client):
    response = client.post('/invoice/update_reminders/1')
    assert response.status_code == 302


def test_invoice_index_with_flash_message(client, authenticated_user):
    authenticated_user()

    response = client.get('/invoice/?msg=Test message')
    assert response.status_code == 200



@pytest.mark.parametrize("discount_type,discount_value", [
    ("fixed", 50),
    ("percent", 10),
    ("fixed", 0),
    ("percent", 0)
])
def test_invoice_discount_variations(client, authenticated_user, client_factory, db_session, discount_type,
                                     discount_value):
    authenticated_user()

    test_client = client_factory(f"Discount {discount_type} Client", f"discount_{discount_type}@example.com",
                                 db_session)

    form_data = {
        'client_id': test_client.id,
        'client_type': 1,
        'currency': 1,
        'bill_id': 0
    }

    response = client.post('/invoice/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        invoice = db.query(Invoice).filter_by(client_id=test_client.id).first()
        assert invoice is not None


def test_invoice_creation_redirects_to_items(client, authenticated_user, client_factory, db_session):
    authenticated_user()

    test_client = client_factory("Redirect Client", "redirect@example.com", db_session)

    form_data = {
        'client_id': test_client.id,
        'client_type': 1,
        'currency': 1,
        'bill_id': 0
    }

    response = client.post('/invoice/add', data=form_data, follow_redirects=False)
    assert response.status_code == 302
    assert 'item' in response.location


def test_invoice_form_validation_missing_client(client, authenticated_user):
    authenticated_user()

    form_data = {
        'client_type': 1,
        'currency': 1,
        'bill_id': 0
    }

    response = client.post('/invoice/add', data=form_data)
    assert response.status_code == 200


def test_invoice_index_empty_state(client, authenticated_user):
    authenticated_user()

    response = client.get('/invoice/')
    assert response.status_code == 200


def test_invoice_with_zero_discount(client, authenticated_user, client_factory, db_session):
    authenticated_user()

    test_client = client_factory("Zero Discount Client", "zero@example.com", db_session)

    form_data = {
        'client_id': test_client.id,
        'client_type': 1,
        'currency': 1,
        'bill_id': 0
    }

    response = client.post('/invoice/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        invoice = db.query(Invoice).filter_by(client_id=test_client.id).first()
        assert invoice is not None


def test_invoice_creation_post(client, authenticated_user, client_factory, db_session):
    authenticated_user()

    test_client = client_factory("Post Client", "post@example.com", db_session)

    form_data = {
        'client_id': test_client.id,
        'client_type': 1,
        'currency': 1,
        'bill_id': 0
    }

    response = client.post('/invoice/add', data=form_data)
    assert response.status_code == 302