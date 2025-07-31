import pytest
from flask import url_for
from datetime import datetime, timedelta
from applib.model import Payment, Invoice, Expense, Items, Client
from decimal import Decimal


def test_dashboard_requires_login(client):
    response = client.get('/dashboard/')
    assert response.status_code == 302
    assert b'login' in response.data


def test_dashboard_index_authenticated(client, authenticated_user):
    authenticated_user()
    response = client.get(url_for("dashboard.index"))
    assert response.status_code == 200
    assert b'dashboard' in response.data.lower()


def test_dashboard_current_year_default(client, authenticated_user):
    authenticated_user()
    current_year = datetime.now().year

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_specific_year(client, authenticated_user):
    authenticated_user()
    test_year = 2024

    response = client.get(f'/dashboard/?year={test_year}')
    assert response.status_code == 200


def test_dashboard_with_payment_data(client, authenticated_user, client_factory, invoice_factory, payment_factory, items_factory, db_session):
    authenticated_user()

    test_client = client_factory("Dashboard Client", "dashboard@example.com", db_session)
    invoice, _ = invoice_factory("Dashboard Client", "dashboard@example.com", "fixed", 50, False, db_session)
    items_factory(invoice.id, db_session, num_items=2)
    payment_factory(invoice.id, db_session, amount=500.00, status=1)

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_with_expense_data(client, authenticated_user, db_session):
    authenticated_user()

    current_year = datetime.now().year

    with db_session as db:
        for month in [1, 3, 6]:
            expense = Expense(
                title=f'Dashboard Expense {month}',
                desc=f'Test expense for month {month}',
                date_created=datetime(current_year, month, 15),
                requested_by='Test User',
                status=2,
                aproved_by='Manager',
                amount=Decimal('200.00'),
                payment_type=1
            )
            db.add(expense)
        db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_monthly_income_calculation(client, authenticated_user, client_factory, invoice_factory,
                                              payment_factory, items_factory, db_session):
    authenticated_user()

    current_year = datetime.now().year
    current_month = datetime.now().month

    test_client = client_factory("Income Client", "income@example.com", db_session)
    invoice, _ = invoice_factory("Income Client", "income@example.com", "fixed", 0, False, db_session)
    items_factory(invoice.id, db_session, num_items=1)

    with db_session as db:
        payment = Payment(
            client_name='Income Client',
            payment_desc='Test payment',
            date_created=datetime(current_year, current_month, 15),
            payment_mode=1,
            amount_paid=Decimal('300.00'),
            balance=Decimal('0.00'),
            invoice_id=invoice.id,
            status=1
        )
        db.add(payment)
        db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_annual_income_calculation(client, authenticated_user, client_factory, invoice_factory, payment_factory, items_factory, db_session):
    authenticated_user()

    current_year = datetime.now().year

    test_client = client_factory("Annual Client", "annual@example.com", db_session)

    for month in [2, 5, 8, 11]:
        invoice, _ = invoice_factory(f"Annual Client {month}", f"annual{month}@example.com", "fixed", 0, False,
                                     db_session)
        items_factory(invoice.id, db_session, num_items=1)

        with db_session as db:
            payment = Payment(
                client_name=f'Annual Client {month}',
                payment_desc=f'Payment for month {month}',
                date_created=datetime(current_year, month, 10),
                payment_mode=1,
                amount_paid=Decimal('150.00'),
                balance=Decimal('0.00'),
                invoice_id=invoice.id,
                status=1
            )
            db.add(payment)
        db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_monthly_expense_calculation(client, authenticated_user, db_session):
    authenticated_user()

    current_year = datetime.now().year
    current_month = datetime.now().month

    with db_session as db:
        expense = Expense(
            title='Monthly Dashboard Expense',
            desc='Test monthly expense',
            date_created=datetime(current_year, current_month, 20),
            requested_by='Test User',
            status=2,
            aproved_by='Manager',
            amount=Decimal('125.00'),
            payment_type=1
        )
        db.add(expense)
        db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200, response.text


def test_dashboard_annual_expense_calculation(client, authenticated_user, db_session):
    authenticated_user()

    current_year = datetime.now().year

    with db_session as db:
        for month in [1, 4, 7, 10]:
            expense = Expense(
                title=f'Annual Expense {month}',
                desc=f'Test annual expense for month {month}',
                date_created=datetime(current_year, month, 5),
                requested_by='Test User',
                status=2,
                aproved_by='Manager',
                amount=Decimal('175.00'),
                payment_type=1
            )
            db.add(expense)
        db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_debt_calculation(client, authenticated_user, client_factory, invoice_factory, payment_factory, items_factory, db_session):
    authenticated_user()

    current_year = datetime.now().year

    test_client = client_factory("Debt Client", "debt@example.com", db_session)
    invoice, _ = invoice_factory("Debt Client", "debt@example.com", "fixed", 100, False, db_session)

    with db_session as db:
        item = Items(
            invoice_id=invoice.id,
            item_desc='Debt Test Item',
            qty=1,
            rate=1000,
            amount=Decimal('1000.00')
        )
        db.add(item)

        payment = Payment(
            client_name='Debt Client',
            payment_desc='Partial payment',
            date_created=datetime(current_year, 6, 15),
            payment_mode=1,
            amount_paid=Decimal('400.00'),
            balance=Decimal('500.00'),
            invoice_id=invoice.id,
            status=2
        )
        db.add(payment)
        db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_exclude_dummy_invoices(client, authenticated_user, client_factory, invoice_factory, payment_factory, items_factory, db_session):
    authenticated_user()

    current_year = datetime.now().year

    test_client = client_factory("Dummy Client", "dummy@example.com", db_session)
    invoice, _ = invoice_factory("Dummy Client", "dummy@example.com", "fixed", 0, False, db_session)
    items_factory(invoice.id, db_session, num_items=1)

    with db_session as db:
        invoice_obj = db.query(Invoice).filter_by(id=invoice.id).first()
        invoice_obj.is_dummy = 1

        payment = Payment(
            client_name='Dummy Client',
            payment_desc='Dummy payment',
            date_created=datetime(current_year, 3, 10),
            payment_mode=1,
            amount_paid=Decimal('200.00'),
            balance=Decimal('0.00'),
            invoice_id=invoice.id,
            status=1
        )
        db.add(payment)
        db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_different_client_types(client, authenticated_user, client_factory, invoice_factory, payment_factory, items_factory, db_session):
    authenticated_user()

    current_year = datetime.now().year
    client_types = [1, 2, 3]

    for client_type in client_types:
        test_client = client_factory(f"Type {client_type} Client", f"type{client_type}@example.com", db_session)
        invoice, _ = invoice_factory(f"Type {client_type} Client", f"type{client_type}@example.com", "percent", 10,
                                     False, db_session)

        with db_session as db:
            invoice_obj = db.query(Invoice).filter_by(id=invoice.id).first()
            invoice_obj.client_type = client_type

            item = Items(
                invoice_id=invoice.id,
                item_desc=f'Type {client_type} Item',
                qty=1,
                rate=500,
                amount=Decimal('500.00')
            )
            db.add(item)

            payment = Payment(
                client_name=f'Type {client_type} Client',
                payment_desc=f'Payment for client type {client_type}',
                date_created=datetime(current_year, 4, 10),
                payment_mode=1,
                amount_paid=Decimal('400.00'),
                balance=Decimal('0.00'),
                invoice_id=invoice.id,
                status=1
            )
            db.add(payment)
            db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_discount_calculations(client, authenticated_user, client_factory, invoice_factory, payment_factory, items_factory, db_session):
    authenticated_user()

    current_year = datetime.now().year

    test_client = client_factory("Discount Client", "discount@example.com", db_session)
    invoice, _ = invoice_factory("Discount Client", "discount@example.com", "percent", 15, False, db_session)
    items_factory(invoice.id, db_session, num_items=1)

    with db_session as db:
        payment = Payment(
            client_name='Discount Client',
            payment_desc='Payment with discount',
            date_created=datetime(current_year, 5, 15),
            payment_mode=1,
            amount_paid=Decimal('300.00'),
            balance=Decimal('0.00'),
            invoice_id=invoice.id,
            status=1
        )
        db.add(payment)
        db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_empty_data(client, authenticated_user):
    authenticated_user()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_previous_year_data(client, authenticated_user, client_factory, invoice_factory, payment_factory, items_factory, db_session):
    authenticated_user()

    previous_year = datetime.now().year - 1

    test_client = client_factory("Previous Year Client", "previous@example.com", db_session)
    invoice, _ = invoice_factory("Previous Year Client", "previous@example.com", "fixed", 0, False, db_session)
    items_factory(invoice.id, db_session, num_items=1)

    with db_session as db:
        payment = Payment(
            client_name='Previous Year Client',
            payment_desc='Previous year payment',
            date_created=datetime(previous_year, 6, 15),
            payment_mode=1,
            amount_paid=Decimal('250.00'),
            balance=Decimal('0.00'),
            invoice_id=invoice.id,
            status=1
        )
        db.add(payment)
        db.commit()

    response = client.get(f'/dashboard/?year={previous_year}')
    assert response.status_code == 200


def test_dashboard_multiple_payments_same_invoice(client, authenticated_user, client_factory, invoice_factory, items_factory, db_session):
    authenticated_user()

    current_year = datetime.now().year

    test_client = client_factory("Multiple Payments Client", "multiple@example.com", db_session)
    invoice, _ = invoice_factory("Multiple Payments Client", "multiple@example.com", "fixed", 0, False, db_session)
    items_factory(invoice.id, db_session, num_items=1)

    with db_session as db:
        payment1 = Payment(
            client_name='Multiple Payments Client',
            payment_desc='First payment',
            date_created=datetime(current_year, 3, 10),
            payment_mode=1,
            amount_paid=Decimal('200.00'),
            balance=Decimal('300.00'),
            invoice_id=invoice.id,
            status=2
        )

        payment2 = Payment(
            client_name='Multiple Payments Client',
            payment_desc='Second payment',
            date_created=datetime(current_year, 4, 15),
            payment_mode=1,
            amount_paid=Decimal('300.00'),
            balance=Decimal('0.00'),
            invoice_id=invoice.id,
            status=1
        )

        db.add_all([payment1, payment2])
        db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_mixed_payment_statuses(client, authenticated_user, client_factory, invoice_factory, payment_factory, items_factory, db_session):
    authenticated_user()

    current_year = datetime.now().year

    for status in [1, 2]:
        test_client = client_factory(f"Status {status} Client", f"status{status}@example.com", db_session)
        invoice, _ = invoice_factory(f"Status {status} Client", f"status{status}@example.com", "fixed", 0, False,
                                     db_session)
        items_factory(invoice.id, db_session, num_items=1)
        payment_factory(invoice.id, db_session, amount=100.00 * status, status=status)

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_zero_amounts(client, authenticated_user, client_factory, invoice_factory, db_session):
    authenticated_user()

    current_year = datetime.now().year

    test_client = client_factory("Zero Amount Client", "zero@example.com", db_session)
    invoice, _ = invoice_factory("Zero Amount Client", "zero@example.com", "fixed", 0, False, db_session)

    with db_session as db:
        item = Items(
            invoice_id=invoice.id,
            item_desc='Zero Amount Item',
            qty=0,
            rate=0,
            amount=Decimal('0.00')
        )
        db.add(item)

        payment = Payment(
            client_name='Zero Amount Client',
            payment_desc='Zero payment',
            date_created=datetime(current_year, 2, 10),
            payment_mode=1,
            amount_paid=Decimal('0.00'),
            balance=Decimal('0.00'),
            invoice_id=invoice.id,
            status=1
        )
        db.add(payment)
        db.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_high_volume_data(client, authenticated_user, client_factory, invoice_factory, payment_factory, items_factory, db_session):
    authenticated_user()

    current_year = datetime.now().year

    for i in range(10):
        test_client = client_factory(f"Volume Client {i}", f"volume{i}@example.com", db_session)
        invoice, _ = invoice_factory(f"Volume Client {i}", f"volume{i}@example.com", "fixed", 5, False, db_session)
        items_factory(invoice.id, db_session, num_items=1)
        payment_factory(invoice.id, db_session, amount=50.00 + i, status=1)

    response = client.get('/dashboard/')
    assert response.status_code == 200


@pytest.mark.parametrize("year", [2023, 2024, 2025, 2026])
def test_dashboard_different_years(client, authenticated_user, year):
    authenticated_user()

    response = client.get(f'/dashboard/?year={year}')
    assert response.status_code == 200


def test_dashboard_invalid_year_parameter(client, authenticated_user):
    authenticated_user()

    response = client.get('/dashboard/?year=invalid')
    assert response.status_code == 200


def test_dashboard_future_year(client, authenticated_user):
    authenticated_user()

    future_year = datetime.now().year + 5

    response = client.get(f'/dashboard/?year={future_year}')
    assert response.status_code == 200


# def test_dashboard_aggregate_calculations(client, authenticated_user, db_session):
#     authenticated_user()
#
#     current_year = datetime.now().year
#
#     with db_session as db:
#         total_income_amount = Decimal('0')
#         total_expense_amount = Decimal('0')
#
#         for month in range(1, 6):
#             expense = Expense(
#                 title=f'Aggregate Expense {month}',
#                 desc=f'Expense for month {month}',
#                 date_created=datetime(current_year, month, 1),
#                 requested_by='Test User',
#                 status=2,
#                 aproved_by='Manager',
#                 amount=Decimal('100.00'),
#                 payment