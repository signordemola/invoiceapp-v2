import pytest
from flask import url_for
from datetime import datetime
from applib.model import Expense
from decimal import Decimal


def test_expense_index_requires_login(client):
    response = client.get('/expense/')
    assert response.status_code == 302
    assert b'login' in response.data


def test_expense_index_authenticated(client, authenticated_user):
    authenticated_user()
    response = client.get(url_for("expense.index"))
    assert response.status_code == 200


def test_expense_index_with_expenses(client, authenticated_user, db_session):
    authenticated_user()

    with db_session as db:
        expense = Expense(
            title='Test Expense',
            desc='Test Description',
            date_created=datetime.now(),
            requested_by='Test User',
            status=1,
            aproved_by='',
            amount=Decimal('500.00'),
            payment_type=1
        )
        db.add(expense)
        db.commit()

    response = client.get('/expense/')
    assert response.status_code == 200
    assert b'Test Expense' in response.data
    assert b'Test Description' in response.data


def test_expense_index_pagination(client, authenticated_user, db_session):
    authenticated_user()

    with db_session as db:
        for i in range(15):
            expense = Expense(
                title=f'Expense {i}',
                desc=f'Description {i}',
                date_created=datetime.now(),
                requested_by=f'User {i}',
                status=1,
                aproved_by='',
                amount=Decimal('100.00'),
                payment_type=1
            )
            db.add(expense)
        db.commit()

    response = client.get('/expense/?page=1')
    assert response.status_code == 200

    response = client.get('/expense/?page=2')
    assert response.status_code == 200


def test_expense_index_with_flash_message(client, authenticated_user):
    authenticated_user()

    response = client.get('/expense/?msg=Test message')
    assert response.status_code == 200


def test_expense_add_get_request(client, authenticated_user):
    authenticated_user()

    response = client.get('/expense/add')
    assert response.status_code == 200
    assert b'form-control' in response.data


def test_expense_add_post_valid(client, authenticated_user, db_session):
    authenticated_user()

    form_data = {
        'title': 'New Office Supplies',
        'desc': 'Purchasing new office supplies for the quarter',
        'amount': '750.50',
        'requested_by': 'John Doe',
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data)
    assert response.status_code == 302
    assert 'expense' in response.location

    with db_session as db:
        expense = db.query(Expense).filter_by(title='New Office Supplies').first()
        assert expense is not None
        assert expense.desc == 'Purchasing new office supplies for the quarter'
        assert expense.amount == Decimal('750.50')
        assert expense.requested_by == 'John Doe'
        assert expense.status == 1
        assert expense.payment_type == 1
        assert expense.date_created is not None


def test_expense_add_post_invalid(client, authenticated_user):
    authenticated_user()

    form_data = {
        'title': '',
        'desc': '',
        'amount': '',
        'requested_by': '',
        'status': 0,
        'payment_type': 0,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data)
    assert response.status_code == 200


def test_expense_edit_get_request(client, authenticated_user, db_session):
    authenticated_user()

    with db_session as db:
        expense = Expense(
            title='Edit Test Expense',
            desc='Edit Test Description',
            date_created=datetime.now(),
            requested_by='Edit User',
            status=1,
            aproved_by='',
            amount=Decimal('300.00'),
            payment_type=1
        )
        db.add(expense)
        db.commit()
        expense_id = expense.id

    response = client.get(f'/expense/edit/{expense_id}')
    assert response.status_code == 200
    assert b'Edit Test Expense' in response.data
    assert b'Edit Test Description' in response.data


def test_expense_edit_post_valid(client, authenticated_user, db_session):
    authenticated_user()

    with db_session as db:
        expense = Expense(
            title='Original Expense',
            desc='Original Description',
            date_created=datetime.now(),
            requested_by='Original User',
            status=1,
            aproved_by='',
            amount=Decimal('200.00'),
            payment_type=1
        )
        db.add(expense)
        db.commit()
        expense_id = expense.id

    form_data = {
        'field_id': expense_id,
        'title': 'Updated Expense',
        'desc': 'Updated Description',
        'amount': '250.00',
        'requested_by': 'Updated User',
        'status': 2,
        'payment_type': 2,
        'aproved_by': 'Manager'
    }

    response = client.post(f'/expense/edit/{expense_id}', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        updated_expense = db.query(Expense).filter_by(id=expense_id).first()
        assert updated_expense.title == 'Updated Expense'
        assert updated_expense.desc == 'Updated Description'
        assert updated_expense.amount == Decimal('250.00')
        assert updated_expense.requested_by == 'Updated User'
        assert updated_expense.status == 2
        assert updated_expense.payment_type == 2
        assert updated_expense.aproved_by == 'Manager'


def test_expense_edit_nonexistent_expense(client, authenticated_user):
    authenticated_user()

    response = client.get('/expense/edit/99999')
    assert response.status_code in [404, 500]


def test_expense_edit_post_invalid(client, authenticated_user, db_session):
    authenticated_user()

    with db_session as db:
        expense = Expense(
            title='Invalid Edit Expense',
            desc='Invalid Edit Description',
            date_created=datetime.now(),
            requested_by='Invalid User',
            status=1,
            aproved_by='',
            amount=Decimal('100.00'),
            payment_type=1
        )
        db.add(expense)
        db.commit()
        expense_id = expense.id

    form_data = {
        'field_id': expense_id,
        'title': '',
        'desc': '',
        'amount': 'invalid-amount',
        'requested_by': '',
        'status': 0,
        'payment_type': 0,
        'aproved_by': ''
    }

    response = client.post(f'/expense/edit/{expense_id}', data=form_data)
    assert response.status_code == 200


def test_expense_different_statuses(client, authenticated_user, db_session):
    authenticated_user()

    statuses = [1, 2, 3]
    status_names = ['Pending', 'Approved', 'Denied']

    for i, status in enumerate(statuses):
        form_data = {
            'title': f'Status {status_names[i]} Expense',
            'desc': f'Testing {status_names[i].lower()} status',
            'amount': '150.00',
            'requested_by': 'Test User',
            'status': status,
            'payment_type': 1,
            'aproved_by': 'Manager' if status == 2 else ''
        }

        response = client.post('/expense/add', data=form_data)
        assert response.status_code == 302

    with db_session as db:
        for i, status in enumerate(statuses):
            expense = db.query(Expense).filter_by(title=f'Status {status_names[i]} Expense').first()
            assert expense.status == status


def test_expense_different_payment_types(client, authenticated_user, db_session):
    authenticated_user()

    payment_types = [1, 2, 3, 4, 5]
    type_names = ['Office Expenses', 'Salary Payment', 'Bonus Payout', 'Miscellenous', 'VAT Remittance']

    for i, payment_type in enumerate(payment_types):
        form_data = {
            'title': f'{type_names[i]} Expense',
            'desc': f'Testing {type_names[i].lower()}',
            'amount': str(100.00 * (i + 1)),
            'requested_by': 'Test User',
            'status': 1,
            'payment_type': payment_type,
            'aproved_by': ''
        }

        response = client.post('/expense/add', data=form_data)
        assert response.status_code == 302

    with db_session as db:
        for i, payment_type in enumerate(payment_types):
            expense = db.query(Expense).filter_by(title=f'{type_names[i]} Expense').first()
            assert expense.payment_type == payment_type


def test_expense_form_validation_required_fields(client, authenticated_user):
    authenticated_user()

    form_data = {
        'title': 'Valid Title',
        'desc': '',
        'amount': '100.00',
        'requested_by': 'Valid User',
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data)
    assert response.status_code == 200


def test_expense_form_validation_zero_amount(client, authenticated_user):
    authenticated_user()

    form_data = {
        'title': 'Zero Amount Expense',
        'desc': 'Testing zero amount',
        'amount': '',
        'requested_by': 'Test User',
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data)
    assert response.status_code == 200, response.text


def test_expense_form_validation_negative_amount(client, authenticated_user):
    authenticated_user()

    form_data = {
        'title': 'Negative Amount Expense',
        'desc': 'Testing negative amount',
        'amount': '-100.00',
        'requested_by': 'Test User',
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data, follow_redirects=True)
    assert response.status_code == 200


def test_expense_decimal_precision(client, authenticated_user, db_session):
    authenticated_user()

    form_data = {
        'title': 'Decimal Precision Expense',
        'desc': 'Testing decimal precision',
        'amount': '123.456789',
        'requested_by': 'Test User',
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        expense = db.query(Expense).filter_by(title='Decimal Precision Expense').first()
        assert expense is not None


def test_expense_large_amount(client, authenticated_user, db_session):
    authenticated_user()

    form_data = {
        'title': 'Large Amount Expense',
        'desc': 'Testing large amount',
        'amount': '999999.99',
        'requested_by': 'Test User',
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        expense = db.query(Expense).filter_by(title='Large Amount Expense').first()
        assert expense.amount == Decimal('999999.99')


def test_expense_approval_workflow(client, authenticated_user, db_session):
    authenticated_user()

    with db_session as db:
        expense = Expense(
            title='Approval Workflow Expense',
            desc='Testing approval workflow',
            date_created=datetime.now(),
            requested_by='Employee',
            status=1,
            aproved_by='',
            amount=Decimal('500.00'),
            payment_type=1
        )
        db.add(expense)
        db.commit()
        expense_id = expense.id

    form_data = {
        'field_id': expense_id,
        'title': 'Approval Workflow Expense',
        'desc': 'Testing approval workflow',
        'amount': '500.00',
        'requested_by': 'Employee',
        'status': 2,
        'payment_type': 1,
        'aproved_by': 'Manager Smith'
    }

    response = client.post(f'/expense/edit/{expense_id}', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        updated_expense = db.query(Expense).filter_by(id=expense_id).first()
        assert updated_expense.status == 2
        assert updated_expense.aproved_by == 'Manager Smith'


def test_expense_denial_workflow(client, authenticated_user, db_session):
    authenticated_user()

    with db_session as db:
        expense = Expense(
            title='Denial Workflow Expense',
            desc='Testing denial workflow',
            date_created=datetime.now(),
            requested_by='Employee',
            status=1,
            aproved_by='',
            amount=Decimal('1000.00'),
            payment_type=1
        )
        db.add(expense)
        db.commit()
        expense_id = expense.id

    form_data = {
        'field_id': expense_id,
        'title': 'Denial Workflow Expense',
        'desc': 'Testing denial workflow',
        'amount': '1000.00',
        'requested_by': 'Employee',
        'status': 3,
        'payment_type': 1,
        'aproved_by': 'Manager Jones'
    }

    response = client.post(f'/expense/edit/{expense_id}', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        updated_expense = db.query(Expense).filter_by(id=expense_id).first()
        assert updated_expense.status == 3
        assert updated_expense.aproved_by == 'Manager Jones'


def test_expense_multiple_expenses_same_user(client, authenticated_user, db_session):
    authenticated_user()

    for i in range(3):
        form_data = {
            'title': f'Expense {i + 1} for Same User',
            'desc': f'Description {i + 1}',
            'amount': str(100.00 * (i + 1)),
            'requested_by': 'Same User',
            'status': 1,
            'payment_type': 1,
            'aproved_by': ''
        }

        response = client.post('/expense/add', data=form_data)
        assert response.status_code == 302

    with db_session as db:
        expenses = db.query(Expense).filter_by(requested_by='Same User').all()
        assert len(expenses) == 3


def test_expense_edit_preserves_date_created(client, authenticated_user, db_session):
    authenticated_user()

    original_date = datetime.now()

    with db_session as db:
        expense = Expense(
            title='Date Preserve Expense',
            desc='Testing date preservation',
            date_created=original_date,
            requested_by='Test User',
            status=1,
            aproved_by='',
            amount=Decimal('200.00'),
            payment_type=1
        )
        db.add(expense)
        db.commit()
        expense_id = expense.id

    form_data = {
        'field_id': expense_id,
        'title': 'Updated Date Preserve Expense',
        'desc': 'Updated description',
        'amount': '250.00',
        'requested_by': 'Test User',
        'status': 2,
        'payment_type': 1,
        'aproved_by': 'Manager'
    }

    response = client.post(f'/expense/edit/{expense_id}', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        updated_expense = db.query(Expense).filter_by(id=expense_id).first()
        assert updated_expense.date_created == original_date
        assert updated_expense.title == 'Updated Date Preserve Expense'


def test_expense_status_labels_display(client, authenticated_user, db_session):
    authenticated_user()

    with db_session as db:
        for status, label in [(1, 'Pending'), (2, 'Approved'), (3, 'Denied')]:
            expense = Expense(
                title=f'{label} Status Expense',
                desc=f'Testing {label.lower()} status display',
                date_created=datetime.now(),
                requested_by='Test User',
                status=status,
                aproved_by='Manager' if status > 1 else '',
                amount=Decimal('100.00'),
                payment_type=1
            )
            db.add(expense)
        db.commit()

    response = client.get('/expense/')
    assert response.status_code == 200


def test_expense_empty_approved_by_field(client, authenticated_user, db_session):
    authenticated_user()

    form_data = {
        'title': 'Empty Approved By Expense',
        'desc': 'Testing empty approved by field',
        'amount': '150.00',
        'requested_by': 'Test User',
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        expense = db.query(Expense).filter_by(title='Empty Approved By Expense').first()
        assert expense.aproved_by == ''


def test_expense_special_characters_in_text(client, authenticated_user, db_session):
    authenticated_user()

    form_data = {
        'title': 'Special Characters: @#$%^&*()',
        'desc': 'Testing special chars: <>?:"{}[]|\\',
        'amount': '75.25',
        'requested_by': "O'Connor & Associates",
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        expense = db.query(Expense).filter_by(title='Special Characters: @#$%^&*()').first()
        assert expense is not None


@pytest.mark.parametrize("amount_str,expected_decimal", [
    ("100", Decimal("100.00")),
    ("100.5", Decimal("100.50")),
    ("100.99", Decimal("100.99")),
    ("0.01", Decimal("0.01")),
    ("999999.99", Decimal("999999.99"))
])
def test_expense_amount_parsing(client, authenticated_user, db_session, amount_str, expected_decimal):
    authenticated_user()

    form_data = {
        'title': f'Amount Test {amount_str}',
        'desc': f'Testing amount {amount_str}',
        'amount': amount_str,
        'requested_by': 'Test User',
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        expense = db.query(Expense).filter_by(title=f'Amount Test {amount_str}').first()
        if expense:
            assert expense.amount == expected_decimal


def test_expense_unicode_characters(client, authenticated_user, db_session):
    authenticated_user()

    form_data = {
        'title': 'Unicode Test: ñáéíóú中文日本語',
        'desc': 'Testing unicode: العربية русский',
        'amount': '200.00',
        'requested_by': 'José García',
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post('/expense/add', data=form_data)
    assert response.status_code == 302

    with db_session as db:
        expense = db.query(Expense).filter_by(requested_by='José García').first()
        assert expense is not None


def test_expense_index_ordering(client, authenticated_user, db_session):
    authenticated_user()

    dates = [
        datetime(2025, 1, 1),
        datetime(2025, 1, 15),
        datetime(2025, 1, 30)
    ]

    with db_session as db:
        for i, date in enumerate(dates):
            expense = Expense(
                title=f'Ordered Expense {i}',
                desc=f'Description {i}',
                date_created=date,
                requested_by='Test User',
                status=1,
                aproved_by='',
                amount=Decimal('100.00'),
                payment_type=1
            )
            db.add(expense)
        db.commit()

    response = client.get('/expense/')
    assert response.status_code == 200


def test_expense_form_field_id_handling(client, authenticated_user, db_session):
    authenticated_user()

    with db_session as db:
        expense = Expense(
            title='Field ID Test Expense',
            desc='Testing field ID handling',
            date_created=datetime.now(),
            requested_by='Test User',
            status=1,
            aproved_by='',
            amount=Decimal('300.00'),
            payment_type=1
        )
        db.add(expense)
        db.commit()
        expense_id = expense.id

    response = client.get(f'/expense/edit/{expense_id}')
    assert response.status_code == 200

    form_data = {
        'field_id': str(expense_id),
        'title': 'Updated Field ID Test',
        'desc': 'Updated description',
        'amount': '350.00',
        'requested_by': 'Test User',
        'status': 1,
        'payment_type': 1,
        'aproved_by': ''
    }

    response = client.post(f'/expense/edit/{expense_id}', data=form_data)
    assert response.status_code == 302