from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from applib.model import RecurrentBill


def test_billing_add_get(client, authenticated_user, db_session, client_factory):
    authenticated_user()
    test_client = client_factory('Test Client', 'test@example.com', db_session)

    response = client.get('/billing/add')
    assert response.status_code == 200


@patch('applib.lib.helper.get_year_range')
@patch('applib.lib.helper.set_pagination')
@patch('applib.lib.helper.date_format')
def test_billing_index_get(mock_date_format, mock_pagination, mock_year_range, client, authenticated_user, db_session, client_factory):
    mock_year_range.return_value = (datetime.now() - timedelta(days=365), datetime.now())
    mock_pagination.return_value = (MagicMock(), [1, 2, 3])
    mock_date_format.return_value = "01-01-2024"

    authenticated_user()
    test_client = client_factory('Test Client', 'test@example.com', db_session)

    response = client.get('/billing/lists')
    assert response.status_code == 200


@patch('applib.lib.helper.get_timeaware')
def test_billing_add_post_valid(mock_timeaware, client, authenticated_user, db_session, client_factory):
    mock_timeaware.return_value = datetime.now()

    authenticated_user()
    test_client = client_factory('Test Client', 'test@example.com', db_session)

    form_data = {
        'client_id': test_client.id,
        'product_name': 'Monthly Service',
        'amount_expected': '299.99',
        'date_due': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    }

    response = client.post('/billing/add', data=form_data, follow_redirects=True)
    assert response.status_code == 200, response.text

    bill = db_session.query(RecurrentBill).filter_by(product_name='Monthly Service').first()
    assert bill is not None
    assert bill.client_id == test_client.id
    assert float(bill.amount_expected) == 299.99


def test_billing_add_post_invalid(client, authenticated_user, db_session):
    authenticated_user()

    form_data = {
        'client_id': '',
        'product_name': '',
        'amount_expected': '',
        'date_due': ''
    }

    response = client.post('/billing/add', data=form_data)
    assert response.status_code == 200

def test_billing_edit_get(client, authenticated_user, db_session, client_factory, recurrent_bill_factory):
    authenticated_user()
    test_client = client_factory('Test Client', 'test@example.com', db_session)
    bill = recurrent_bill_factory(test_client.id, db_session)

    response = client.get(f'/billing/edit/{bill.id}')
    assert response.status_code == 200


@patch('applib.lib.helper.get_current_timezone')
def test_billing_edit_post_valid(mock_timezone, client, authenticated_user, db_session, client_factory, recurrent_bill_factory):
    mock_timezone.return_value = datetime.now()

    authenticated_user()
    test_client = client_factory('Test Client', 'test@example.com', db_session)
    bill = recurrent_bill_factory(test_client.id, db_session)

    form_data = {
        'client_id': test_client.id,
        'product_name': 'Updated Service',
        'amount_expected': '399.99',
        'date_due': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d')
    }

    response = client.post(f'/billing/edit/{bill.id}', data=form_data, follow_redirects=True)
    assert response.status_code == 200, response.text

    db_session.refresh(bill)
    assert bill.product_name == 'Updated Service'
    assert float(bill.amount_expected) == 399.99

@patch('applib.lib.helper.get_year_range')
@patch('applib.lib.helper.set_pagination')
def test_billing_index_pagination(mock_pagination, mock_year_range, client, authenticated_user, db_session, client_factory, recurrent_bill_factory):
    mock_year_range.return_value = (datetime.now() - timedelta(days=365), datetime.now())
    mock_pagination.return_value = (MagicMock(), [1, 2])

    authenticated_user()
    test_client = client_factory('Test Client', 'test@example.com', db_session)

    for i in range(5):
        recurrent_bill_factory(test_client.id, db_session)

    response = client.get('/billing/lists?page=1')
    assert response.status_code == 200

    response = client.get('/billing/lists?page=2')
    assert response.status_code == 200


@patch('applib.lib.helper.get_year_range')
@patch('applib.lib.helper.set_pagination')
def test_billing_with_payments(mock_pagination, mock_year_range, client, authenticated_user, db_session, client_factory, invoice_factory, payment_factory):
    mock_year_range.return_value = (datetime.now() - timedelta(days=365), datetime.now())
    mock_pagination.return_value = (MagicMock(), [1])

    authenticated_user()

    invoice, test_client = invoice_factory('Test Client', 'test@example.com', 'fixed', 10, True, db_session)
    payment = payment_factory(invoice.id, db_session, 500.00, 1)

    bill = RecurrentBill(
        client_id=test_client.id,
        invoice_id=invoice.id,
        product_name='Service with Payment',
        amount_expected=500.00,
        date_created=datetime.now(),
        date_due=datetime.now() + timedelta(days=30),
        date_updated=datetime.now(),
        payment_status=0
    )
    db_session.add(bill)
    db_session.commit()

    response = client.get('/billing/lists')
    assert response.status_code == 200


@patch('applib.lib.helper.get_year_range')
@patch('applib.lib.helper.set_pagination')
def test_billing_status_calculations(mock_pagination, mock_year_range, client, authenticated_user, db_session, client_factory, recurrent_bill_factory):
    mock_year_range.return_value = (datetime.now() - timedelta(days=365), datetime.now())
    mock_pagination.return_value = (MagicMock(), [1])

    authenticated_user()
    test_client = client_factory('Test Client', 'test@example.com', db_session)

    bill1 = recurrent_bill_factory(test_client.id, db_session)
    bill2 = recurrent_bill_factory(test_client.id, db_session)
    bill2.payment_status = -1
    db_session.commit()

    response = client.get('/billing/lists')
    assert response.status_code == 200

def test_billing_form_validation(client, authenticated_user, db_session, client_factory):
    authenticated_user()
    test_client = client_factory('Test Client', 'test@example.com', db_session)

    form_data = {
        'client_id': 99999,
        'product_name': 'Test Service',
        'amount_expected': 'invalid_amount',
        'date_due': ''
    }

    response = client.post('/billing/add', data=form_data)
    assert response.status_code == 200, response.text

@patch('applib.lib.helper.get_year_range')
@patch('applib.lib.helper.set_pagination')
def test_billing_empty_database(mock_pagination, mock_year_range, client, authenticated_user, db_session):
    mock_year_range.return_value = (datetime.now() - timedelta(days=365), datetime.now())
    mock_pagination.return_value = (MagicMock(), [1])

    authenticated_user()

    response = client.get('/billing/lists')
    assert response.status_code == 200


@patch('applib.lib.helper.get_year_range')
@patch('applib.lib.helper.set_pagination')
@patch('applib.lib.helper.date_format')
def test_billing_index_with_data(mock_date_format, mock_pagination, mock_year_range, client, authenticated_user, db_session, client_factory, recurrent_bill_factory):
    mock_year_range.return_value = (datetime.now() - timedelta(days=365), datetime.now())
    mock_pagination.return_value = (MagicMock(), [1, 2, 3])
    mock_date_format.return_value = "01-01-2024"

    authenticated_user()
    test_client = client_factory('Test Client', 'test@example.com', db_session)
    bill = recurrent_bill_factory(test_client.id, db_session)

    response = client.get('/billing/lists')
    assert response.status_code == 200, response.text


@patch('applib.lib.helper.get_year_range')
@patch('applib.lib.helper.set_pagination')
def test_billing_date_range_filter(mock_pagination, mock_year_range, client, authenticated_user, db_session, client_factory, recurrent_bill_factory):
    mock_year_range.return_value = (datetime.now() - timedelta(days=365), datetime.now())
    mock_pagination.return_value = (MagicMock(), [1])

    authenticated_user()
    test_client = client_factory('Test Client', 'test@example.com', db_session)

    old_bill = recurrent_bill_factory(test_client.id, db_session)
    old_bill.date_created = datetime.now() - timedelta(days=400)
    db_session.commit()

    response = client.get('/billing/lists')
    assert response.status_code == 200


@patch('applib.lib.helper.get_year_range')
@patch('applib.lib.helper.set_pagination')
def test_billing_multiple_clients(mock_pagination, mock_year_range, client, authenticated_user, db_session, client_factory, recurrent_bill_factory):
    mock_year_range.return_value = (datetime.now() - timedelta(days=365), datetime.now())
    mock_pagination.return_value = (MagicMock(), [1])

    authenticated_user()

    client1 = client_factory('Client One', 'client1@example.com', db_session)
    client2 = client_factory('Client Two', 'client2@example.com', db_session)

    bill1 = recurrent_bill_factory(client1.id, db_session)
    bill2 = recurrent_bill_factory(client2.id, db_session)

    response = client.get('/billing/lists')
    assert response.status_code == 200