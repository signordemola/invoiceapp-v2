
from datetime import datetime

from flask import (Blueprint, request, url_for, 
                   render_template, redirect, session, 
                   flash
                )

from flask_login import login_required 

from sqlalchemy import func, update 

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


from applib.model import sql_cursor, RecurrentBill, Invoice, Client, Payment

from applib.forms import BillingFrm
from applib.lib.helper import (
    get_config, date_format, set_pagination, 
    get_timeaware, get_year_range, get_current_timezone
)


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

mod = Blueprint('billing', __name__, url_prefix='/billing')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@mod.route('/lists')
@login_required
def index() -> str:

    cur_page = request.args.get('page', 1, int)

    with sql_cursor() as db:

        recent_payments = db.query(
            Payment.invoice_id,
            func.max(Payment.status).label('status'),
            func.sum(Payment.amount_paid).label('amount_paid')
        ).group_by(Payment.invoice_id).subquery()

        qry = db.query(
                RecurrentBill.id,
                Client.name.label('client'),
                Client.id.label('client_id'),
                Invoice.invoice_no,
                RecurrentBill.product_name,
                RecurrentBill.amount_expected,
                RecurrentBill.date_created,
                RecurrentBill.date_due,
                RecurrentBill.payment_status,
                recent_payments.c.amount_paid, 
                recent_payments.c.status
            ).outerjoin(
                Invoice, Invoice.id == RecurrentBill.invoice_id
            ).outerjoin(
                recent_payments, recent_payments.c.invoice_id == RecurrentBill.invoice_id
            ).join(
                Client, Client.id == RecurrentBill.client_id 
            ).order_by(RecurrentBill.id.desc())

        qry, page_row = set_pagination(qry, cur_page, page_size=20)    


        start, stop = get_year_range()

        agg_calculation = db.query(       
            RecurrentBill.invoice_id,
            func.max(RecurrentBill.payment_status).label('payment_status'),
            func.max(RecurrentBill.amount_expected).label('amount_expected'),
            func.sum(Payment.amount_paid).label('amount')
        ).outerjoin(
            Payment, 
            Payment.invoice_id == RecurrentBill.invoice_id
        ).group_by(
            RecurrentBill.invoice_id
        ).where(
            RecurrentBill.date_created.between(start, stop)            
        ).all()

        print(agg_calculation) 


    paid, potential, cancelled  = 0, 0, 0

    for row in agg_calculation:

        if not row.amount:
            if row.payment_status == 0:
                potential += row.amount_expected 
                
            elif row.payment_status == -1:
                cancelled += row.amount_expected 

        elif row.amount >= row.amount_expected:
            paid += float(row.amount) 

        elif row.amount < row.amount_expected:
            paid += row.amount 
            potential = row.amount_expected - float(row.amount) 

    print(agg_calculation, '\n\n')


    def confirm_status(amount_paid:float, amount_expected:float, _status:int) -> int:
        
        if not amount_paid:
            return _status

        if amount_paid >= amount_expected:
            return RecurrentBill.STATUSTYPE.processed
        elif amount_paid < amount_expected:
            return RecurrentBill.STATUSTYPE.in_progress

        return _status

    return render_template(
        "billing.html", 
        pager=qry, 
        check_status=confirm_status,
        page_row=page_row, cur_page=cur_page,
        date_format=date_format, 
        payment_stages={
            'paid': paid, 
            'cancelled': cancelled, 
            'potential': potential
        })



@mod.route('/add', methods=['GET', 'POST'])
@login_required
def add_billing_view() -> str:

    form = BillingFrm(**request.form)

    with sql_cursor() as db:
        qry = db.query(Client.id, Client.name).order_by(Client.id.desc()).all()
        form.client_id.choices.extend(qry)

    
    form.date_due.process_formdata([form.date_due.data] if form.date_due.data else [])

    if request.method == 'POST' and form.validate():
        # add the billing form here         

        rebill = RecurrentBill()        

        ex_fields = ['id', 'date_created', 'date_due']

        for name, field in form._fields.items():

            if name in ex_fields:
                continue

            if hasattr(rebill, name):
                setattr(rebill, name, field.data)
        
        rebill.date_due = form.date_due.data 
        rebill.date_created = get_timeaware(datetime.now())
        rebill.payment_status = rebill.STATUSTYPE.pending

        with sql_cursor() as db:
            db.add(rebill)

        return redirect(url_for('billing.index'))

        
    return render_template('add_billing.html', form=form)




# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_billing_view(id: int) -> str:

    form = BillingFrm(**request.form)

    with sql_cursor() as db:
        qry = db.query(Client.id, Client.name).order_by(Client.id.desc()).all()
        form.client_id.choices.extend(qry)
        bill_data = db.query(RecurrentBill).get(id)

        if request.method == 'GET':
            for name, field in form._fields.items():
                if hasattr(bill_data, name):
                    field.data = getattr(bill_data, name)

    if form.date_due.data and isinstance(form.date_due.data, str):
        form.date_due.process_formdata([form.date_due.data])

    

    if request.method == 'POST' and form.validate():

        with sql_cursor() as db:
            db.execute(
                update(RecurrentBill)
                .where(RecurrentBill.id == id)
                .values({
                    'date_due': form.date_due.data,
                    'amount_expected': form.amount_expected.data,
                    'product_name': form.product_name.data,
                    'client_id': form.client_id.data,
                    'date_updated': get_current_timezone()
                })
            )

        return redirect(url_for('billing.index'))

    return render_template('add_billing.html', form=form)