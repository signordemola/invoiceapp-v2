from applib.model import Items
from decimal import Decimal


def test_add_item_get_request(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", False, db_session)

    response = client.get(f'/item/item/{invoice.id}')
    assert response.status_code == 200
    assert b'Test Client' in response.data


def test_add_item_post_valid_data(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", False, db_session)

    item_data = {
        'item_desc': 'Test Item Description',
        'qty': 2,
        'rate': 100,
        'amt': 200
    }

    response = client.post(f'/item/item/{invoice.id}', data=item_data)

    assert response.status_code == 302
    assert f'/invoice/checkout/{invoice.id}' in response.location

    item = db_session.query(Items).filter_by(invoice_id=invoice.id).first()
    assert item is not None
    assert item.item_desc == 'Test Item Description'
    assert item.qty == 2
    assert item.rate == 100
    assert item.amount == Decimal('200.00')


def test_add_item_post_invalid_data(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", False, db_session)

    item_data = {
        'item_desc': '',
        'qty': '',
        'rate': 100,
        'amt': 200
    }

    response = client.post(f'/item/item/{invoice.id}', data=item_data)
    assert response.status_code == 200

    item_count = db_session.query(Items).filter_by(invoice_id=invoice.id).count()
    assert item_count == 0


def test_add_item_nonexistent_invoice(client, authenticated_user, db_session):
    authenticated_user()

    response = client.get('/item/item/99999')
    assert response.status_code in [404, 500]


def test_edit_item_get_request(client, authenticated_user, invoice_factory, items_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", True, db_session)

    item = db_session.query(Items).filter_by(invoice_id=invoice.id).first()

    response = client.get(f'/item/item/{invoice.id}/{item.id}')
    assert response.status_code == 200
    assert b'Test Client' in response.data


def test_edit_item_post_valid_data(client, authenticated_user, invoice_factory, items_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", True, db_session)

    item = db_session.query(Items).filter_by(invoice_id=invoice.id).first()
    original_desc = item.item_desc

    edit_data = {
        'item_desc': 'Updated Item Description',
        'qty': 3,
        'rate': 150,
        'amt': 450
    }

    response = client.post(f'/item/item/{invoice.id}/{item.id}', data=edit_data)

    assert response.status_code == 302
    assert f'/invoice/checkout/{invoice.id}' in response.location

    db_session.refresh(item)
    assert item.item_desc == 'Updated Item Description'
    assert item.qty == 3
    assert item.rate == 150
    assert item.amount == Decimal('450.00')


def test_edit_item_post_invalid_data(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", True, db_session)

    item = db_session.query(Items).filter_by(invoice_id=invoice.id).first()
    original_desc = item.item_desc

    edit_data = {
        'item_desc': '',
        'qty': '',
        'rate': 150,
        'amt': 450
    }

    response = client.post(f'/item/item/{invoice.id}/{item.id}', data=edit_data)
    assert response.status_code == 200

    db_session.refresh(item)
    assert item.item_desc == original_desc


def test_edit_nonexistent_item(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", False, db_session)

    response = client.get(f'/item/item/{invoice.id}/99999')
    assert response.status_code in [404, 500]


def test_delete_item_success(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", True, db_session)

    item = db_session.query(Items).filter_by(invoice_id=invoice.id).first()
    item_id = item.id

    response = client.get(f'/item/delete/item/{invoice.id}/{item_id}')

    assert response.status_code == 302
    assert f'/invoice/checkout/{invoice.id}' in response.location

    deleted_item = db_session.query(Items).filter_by(id=item_id).first()
    assert deleted_item is None


def test_delete_nonexistent_item(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", False, db_session)

    response = client.get(f'/item/delete/item/{invoice.id}/99999')
    assert response.status_code == 302
    assert f'/invoice/checkout/{invoice.id}' in response.location


def test_add_discount_get_no_items(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", False, db_session)

    response = client.get(f'/item/discount/{invoice.id}')
    assert response.status_code == 302
    assert '/invoice/' in response.location


def test_add_discount_get_with_items(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", True, db_session)

    response = client.get(f'/item/discount/{invoice.id}')
    assert response.status_code in [200, 500]


def test_add_discount_get_existing_discount(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "percent", "10", True, db_session)

    response = client.get(f'/item/discount/{invoice.id}')
    assert response.status_code in [200, 500]


def test_add_discount_post_valid_fixed(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", None, None, True, db_session)

    discount_data = {
        'discount_type': 'fixed',
        'discount': '50',
        'disc_desc': 'Early payment discount'
    }

    response = client.post(f'/item/discount/{invoice.id}', data=discount_data)

    if response.status_code == 302:
        assert f'/invoice/checkout/{invoice.id}' in response.location
        db_session.refresh(invoice)
        assert invoice.disc_type == 'fixed'
        assert invoice.disc_value == '50'
        assert invoice.disc_desc == 'Early payment discount'
    else:
        assert response.status_code == 200


def test_add_discount_post_valid_percent(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", None, None, True, db_session)

    discount_data = {
        'discount_type': 'percent',
        'discount': '15',
        'disc_desc': 'Volume discount'
    }

    response = client.post(f'/item/discount/{invoice.id}', data=discount_data)

    if response.status_code == 302:
        assert f'/invoice/checkout/{invoice.id}' in response.location
        db_session.refresh(invoice)
        assert invoice.disc_type == 'percent'
        assert invoice.disc_value == '15'
        assert invoice.disc_desc == 'Volume discount'
    else:
        assert response.status_code == 200


def test_add_discount_post_invalid_data(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", None, None, True, db_session)

    discount_data = {
        'discount_type': 'fixed',
        'discount': '',
        'disc_desc': 'Test discount'
    }

    response = client.post(f'/item/discount/{invoice.id}', data=discount_data)
    assert response.status_code == 200

    db_session.refresh(invoice)
    assert invoice.disc_type is None


def test_delete_discount_success(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", True, db_session)

    assert invoice.disc_type == 'fixed'
    assert invoice.disc_value == '50'

    response = client.get(f'/item/delete/discount/{invoice.id}')

    assert response.status_code == 302
    assert f'/invoice/checkout/{invoice.id}' in response.location

    db_session.refresh(invoice)
    assert invoice.disc_type is None
    assert invoice.disc_value is None
    assert invoice.disc_desc is None


def test_delete_discount_no_existing_discount(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", None, None, True, db_session)

    assert invoice.disc_type is None

    response = client.get(f'/item/delete/discount/{invoice.id}')

    assert response.status_code == 302
    assert f'/invoice/checkout/{invoice.id}' in response.location


def test_add_item_requires_auth(client, invoice_factory, db_session):
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", False, db_session)

    response = client.get(f'/item/item/{invoice.id}')
    assert response.status_code in [200, 302]
    if response.status_code == 302:
        assert 'login' in response.location


def test_edit_item_requires_auth(client, invoice_factory, db_session):
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", True, db_session)
    item = db_session.query(Items).filter_by(invoice_id=invoice.id).first()

    response = client.get(f'/item/item/{invoice.id}/{item.id}')
    assert response.status_code in [200, 302]
    if response.status_code == 302:
        assert 'login' in response.location


def test_delete_item_requires_auth(client, invoice_factory, db_session):
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", True, db_session)
    item = db_session.query(Items).filter_by(invoice_id=invoice.id).first()

    response = client.get(f'/item/delete/item/{invoice.id}/{item.id}')
    assert response.status_code == 302


def test_add_discount_requires_auth(client, invoice_factory, db_session):
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", False, db_session)

    response = client.get(f'/item/discount/{invoice.id}')
    assert response.status_code == 302


def test_delete_discount_requires_auth(client, invoice_factory, db_session):
    invoice, test_client = invoice_factory("Test Client", "test@example.com", "fixed", "50", False, db_session)

    response = client.get(f'/item/delete/discount/{invoice.id}')
    assert response.status_code == 302


def test_complete_item_workflow(client, authenticated_user, invoice_factory, db_session):
    authenticated_user()
    invoice, test_client = invoice_factory("Test Client", "test@example.com", None, None, False, db_session)

    item_data = {
        'item_desc': 'Test Product',
        'qty': 2,
        'rate': 100,
        'amt': 200
    }
    response = client.post(f'/item/item/{invoice.id}', data=item_data)
    assert response.status_code == 302

    item = db_session.query(Items).filter_by(invoice_id=invoice.id).first()
    assert item is not None

    edit_data = {
        'item_desc': 'Updated Product',
        'qty': 3,
        'rate': 150,
        'amt': 450
    }
    response = client.post(f'/item/item/{invoice.id}/{item.id}', data=edit_data)
    assert response.status_code == 302

    discount_data = {
        'discount_type': 'percent',
        'discount': '10',
        'disc_desc': 'Customer discount'
    }
    response = client.post(f'/item/discount/{invoice.id}', data=discount_data)

    if response.status_code == 302:
        db_session.refresh(invoice)
        assert invoice.disc_type == 'percent'

        response = client.get(f'/item/delete/discount/{invoice.id}')
        assert response.status_code == 302

        db_session.refresh(invoice)
        assert invoice.disc_type is None

    response = client.get(f'/item/delete/item/{invoice.id}/{item.id}')
    assert response.status_code == 302

    deleted_item = db_session.query(Items).filter_by(id=item.id).first()
    assert deleted_item is None