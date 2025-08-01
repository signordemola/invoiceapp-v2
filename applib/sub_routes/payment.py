
from flask import (Blueprint, request, url_for, 
                   render_template, redirect, flash)

from sqlalchemy import update, func


import applib.model as m
from applib.forms import PaymentForm, CreateInvoiceForm
from applib.lib import helper as h 
from applib.lib.helper import (
    generate_pdf, get_current_timezone,
    comma_separation, set_pagination
)

from flask_login import login_required
from datetime import datetime



mod = Blueprint('payment', __name__, url_prefix='/payment')

@mod.route("/")
@login_required
def index():
    form = PaymentForm(request.form)
    status = { x[0]: x[1] for x in form.status.choices}
    cur_page = request.args.get('page', 1, int)
    month_filter = request.args.get('filtermonth', None)

    start, end = None, None 

    if month_filter:
        year, mon, day = month_filter.split('-')

        start, end = h.get_month_range(int(year), int(mon))
 

    with m.sql_cursor() as db:

        description = db.query(
                                m.Payment.invoice_id, 
                                func.max(m.Payment.id).label('pid'),
                                func.sum(m.Payment.amount_paid).label("paid")
                            ).group_by(m.Payment.invoice_id).subquery()

        sub = db.query(m.Items.invoice_id,
                               func.sum(m.Items.amount                                              
                                          ).label("sub_total"),
                               ).group_by(
                                    m.Items.invoice_id
                               ).subquery()

        qry = db.query(
                        m.Invoice.invoice_no,
                        m.Invoice.id,
                        m.Invoice.disc_type, 
                        m.Invoice.disc_value,
                        m.Invoice.client_type,
                        description.c.pid,                        
                        description.c.paid,
                        description.c.invoice_id,
                        sub.c.sub_total,
                        m.Payment.payment_desc,
                        m.Payment.date_created,
                        m.Payment.payment_mode,
                        m.Payment.status, 
                        m.Payment.id.label("pid"),
                        m.Client.name   
                    ).join(
                        description,
                        description.c.invoice_id == m.Invoice.id                 
                    ).outerjoin(sub, 
                        sub.c.invoice_id == m.Invoice.id
                    ).join(
                        m.Payment,
                        m.Payment.id == description.c.pid
                    ).join(m.Client,
                           m.Client.id == m.Invoice.client_id                    
                    ).order_by(description.c.pid.desc())

        total_amount = db.query(func.sum(m.Payment.amount_paid).label("paid"))


        if start and end:
            qry = qry.filter(m.Payment.date_created.between(start, end))
            total_amount = total_amount.filter(m.Payment.date_created.between(start, end))

        total_amount= total_amount.scalar()

        qry, page_row = set_pagination(qry, cur_page)

        grp_data = []

        for x in qry.items:
            retv = {}

            retv['id'] = x.pid
            retv['invoice_id'] = x.invoice_id
            retv['inv_id'] = x.id
            retv['date_created'] = x.date_created 
            retv['name'] = x.name 
            retv['payment_desc'] = x.payment_desc
            

            vat_total, vat, total, discount = h.val_calculated_data(x.disc_type, x.disc_value, 
                                                                    x.sub_total, x.client_type)

            retv['balance'] = h.float2decimal(vat_total) - x.paid
            retv['status'] = 1 if (x.paid - h.float2decimal(vat_total)) == 0 else 2 

            grp_data.append(retv)

        cur_fmt = comma_separation                                  


    msg = request.args.get("msg")
    if msg:
        flash(msg)


    return render_template('payment.html', pager=qry, status_label=status,
                            date_format=h.date_format, data=grp_data, 
                            page_row=page_row, cur_page=cur_page, 
                            cur_fmt=cur_fmt, total_paid=total_amount
                           )


@mod.route("/add/<int:invoice_id>/<invoice_name>", methods=["POST", "GET"])
@login_required
def add(invoice_id, invoice_name):
    
    form = PaymentForm(request.form, client_name=invoice_name)
    form_inv = CreateInvoiceForm()
    currency_label = {x[0]: x[1] for x in form_inv.currency.choices} 
    
    with m.sql_cursor() as db:
        item_details = db.query(m.Items.amount, m.Items.item_desc).filter_by(
                                                        invoice_id=invoice_id
                                                        ).all()
        invoice_query = db.query(m.Invoice.id,
                                 m.Invoice.disc_type, 
                                 m.Invoice.disc_value,
                                 m.Invoice.client_type,
                                 m.Invoice.currency).filter_by(id=invoice_id
                                                               ).first()

        data = {}

        _amount = 0

        for x in item_details:
            _amount += x.amount

        vat_total, vat, total, discount = h.val_calculated_data(invoice_query.disc_type, 
                                                                invoice_query.disc_value, 
                                                                _amount, 
                                                                invoice_query.client_type)
        
        data['sub_total'] = total
        data['vat'] = vat

        data['cur_fmt'] = comma_separation
        data['currency'] = currency_label[invoice_query.currency]    
    

        if request.method == 'POST' and form.validate():
            pay_md = m.Payment()
            m.form2model(form, pay_md)
            pay_md.invoice_id = invoice_id

            pay_md.date_created = datetime.now()
            db.add(pay_md)
            db.commit()
 
            total_payment = db.query(
                    func.sum(m.Payment.amount_paid).label('amount')
                ).filter(m.Payment.invoice_id == invoice_id).first()


            check_recurrent_bill = db.query(
                m.RecurrentBill.id, m.RecurrentBill.amount_expected
            ).filter(m.RecurrentBill.invoice_id == invoice_id).first()



            if check_recurrent_bill and check_recurrent_bill.amount_expected >= total_payment.amount:

                db.execute(
                    update(m.RecurrentBill)
                    .where( m.RecurrentBill.invoice_id == invoice_id )
                    .values({'payment_status': m.RecurrentBill.STATUSTYPE.processed, 'date_updated': get_current_timezone()})
                )

            elif check_recurrent_bill and check_recurrent_bill.amount_expected < total_payment.amount:
                db.execute(
                    update(m.RecurrentBill)
                    .where( m.RecurrentBill.invoice_id == invoice_id )
                    .values({'payment_status': m.RecurrentBill.STATUSTYPE.in_progress, 'date_updated': get_current_timezone()})
                )


            msg = "Payment has being Added"
            return redirect(url_for('payment.index', msg=msg))

    return render_template('add_payment.html', 
                           form=form, 
                           title="Add Payment",
                           discount=discount,
                           total=vat_total,
                           subtotal=total,
                           vat=vat,
                           item_details=item_details,
                           kwargs=data,
                           invoice_query=invoice_query)
    


@mod.route("/edit/<int:pay_id>/<int:invoice_id>", methods=["POST", "GET"])
@login_required
def edit(pay_id, invoice_id):

    form = PaymentForm(**request.form)

    payment_mode_label = {x[0]: x[1] for x in form.payment_mode.choices}
    status_label = {x[0]: x[1] for x in form.status.choices}
    currency_label = {x[0]: x[1] for x in CreateInvoiceForm().currency.choices}

    if request.method == 'POST' and form.validate():
        
        with m.sql_cursor() as db:
            pay_md = m.Payment()
            m.form2model(form, pay_md)
            pay_md.invoice_id = invoice_id
            pay_md.date_created = datetime.now()
            db.add(pay_md)
        
        return redirect(url_for("payment.index", msg='Paymemt updated successfully.'))

    with m.sql_cursor() as db:

        item_details = db.query(m.Items.invoice_id, func.sum(m.Items.amount).label('total_amount')
                                ).group_by(m.Items.invoice_id).subquery()

        prev_amount_paid = db.query(m.Payment.invoice_id, 
                                    func.sum(m.Payment.amount_paid).label('total_paid')
                                    ).group_by(m.Payment.invoice_id).subquery()


        invoice_data = db.query(m.Invoice.id, 
                                 m.Invoice.disc_type, 
                                 m.Invoice.disc_value,
                                 m.Invoice.client_type,
                                 m.Invoice.currency,
                                 m.Client.name,
                                 item_details.c.total_amount,
                                 prev_amount_paid.c.total_paid
                                ).join(
                                    m.Client,
                                    m.Client.id == m.Invoice.client_id
                                ).join(
                                    item_details, 
                                    item_details.c.invoice_id == invoice_id 
                                ).join(
                                    prev_amount_paid,
                                    prev_amount_paid.c.invoice_id == invoice_id
                                ).filter(m.Invoice.id == invoice_id).first()
 
        payment_history = db.query(m.Payment
                                   ).filter(
                                    m.Payment.invoice_id == invoice_id
                                   )


        def calc_balance(amount, total):
            return total - amount

        
        vat_total, vat, total, discount = h.val_calculated_data(invoice_data.disc_type, 
                                        invoice_data.disc_value, 
                                        invoice_data.total_amount, 
                                        invoice_data.client_type)


        payment_agg = []

        dynamic_amt = h.float2decimal(0) 
        cur_balance = h.float2decimal(0)  


        for x in payment_history.all():
            
            dynamic_amt += x.amount_paid
            cur_balance = calc_balance(dynamic_amt, h.float2decimal(vat_total))
            tmp = {
                "date_created":x.date_created,
                "amount_paid":x.amount_paid,
                "payment_mode":x.payment_mode,
                "balance":cur_balance,
                "status":status_label[x.status]
            }

            payment_agg.append(tmp)


        item_data = db.query(m.Items).filter(m.Items.invoice_id == invoice_id)


        form.client_name.data = invoice_data.name
        form.balance.data = cur_balance


        retv = dict(
            form=form, title="Add Payment", discount=discount,
            total=vat_total, subtotal=total, vat=vat,
            pay_lbl=payment_mode_label, stat_lbl=status_label,
            cur_lbl=currency_label, payments=payment_agg,
            items=item_data, invoice_data=invoice_data, 
            cur_balance=cur_balance
        )
    

    return render_template("edit_payment.html", **retv)
                            



@mod.route("/receipt/<int:invoice_id>", methods=['POST', 'GET'])
@login_required
def receipt(invoice_id):

    form_pay = PaymentForm()
    status = {x[0]: x[1] for x in form_pay.status.choices}

    form_inv = CreateInvoiceForm()
    currency_label = {x[0]: x[1] for x in form_inv.currency.choices}

    with m.sql_cursor() as db:

        aggr_amount_paid = db.query(
                                m.Payment.invoice_id, 
                                func.sum(m.Payment.amount_paid).label("paid")
                            ).group_by(m.Payment.invoice_id).subquery()

        client_invoice_details = db.query(m.Invoice.id.label("invoice_id"),
                                          m.Invoice.invoice_no, 
                                          m.Invoice.disc_value,
                                          m.Invoice.disc_type, 
                                          m.Invoice.currency,
                                          m.Invoice.client_type,
                                          m.Payment.id.label('payment_id'),
                                          m.Payment.amount_paid, 
                                          m.Payment.status, 
                                          m.Payment.date_created,
                                          aggr_amount_paid.c.paid,
                                          m.Payment.balance, 
                                          m.Client.address,
                                          m.Client.post_addr, 
                                          m.Client.name,
                                          m.Client.email, m.Client.phone
                                        ).join(m.Payment,
                                               m.Payment.invoice_id == m.Invoice.id
                                        ).join(m.Client,
                                               m.Client.id == m.Invoice.client_id
                                        ).join(aggr_amount_paid,
                                               aggr_amount_paid.c.invoice_id == m.Invoice.id
                                               ).filter(
                                                    m.Invoice.id == invoice_id
                                                    ).first()

        data = {
                'invoice_no': client_invoice_details.invoice_no,
                'date_value': client_invoice_details.date_created.strftime("%Y-%m-%d"),
                'address': client_invoice_details.address,
                'post_addr': client_invoice_details.post_addr,
                'name': client_invoice_details.name,
                'email': client_invoice_details.email,
                'phone': client_invoice_details.phone,
                'refid': client_invoice_details.payment_id,
                'reftype': 'payment'
            }

        data['cur_fmt'] = comma_separation

        item_for_amount = db.query(
                                    m.Items.id,
                                    m.Items.item_desc,
                                    m.Items.qty,
                                    m.Items.rate,
                                    m.Items.amount
                                ).filter_by(invoice_id=invoice_id).all()

        items = []
        for y in item_for_amount:
            items.append({
                            'id': y.id, 'item_desc': y.item_desc,
                            'qty': y.qty, 'rate': y.rate, 'amount': y.amount
                        })

        _amount = 0
        
        for x in item_for_amount:
            _amount += x.amount


        # for x in client_invoice_details:
        
        vat_total, vat, total, discount = h.val_calculated_data(
            client_invoice_details.disc_type, client_invoice_details.disc_value, 
            _amount, client_invoice_details.client_type)

        data['amount_paid'] = client_invoice_details.paid
        data['amount_balance'] = h.float2decimal(vat_total) - client_invoice_details.paid
        data['subtotal'] = total
        data['vat'] = vat
        data['total'] = vat_total
        data['status'] = status[client_invoice_details.status]
        data['currency'] = currency_label[client_invoice_details.currency]


        data['type'] = "Receipt"

        payment_history = db.query(m.Payment.date_created,
                                   m.Payment.amount_paid
                                   ).filter(
                                    m.Payment.invoice_id == invoice_id
                                   ).all()

        def calc_balance(amount, total):
            return total - amount

        dynamic_amt = h.float2decimal(0) 
        cur_balance = h.float2decimal(0)

        payment_agg = []
        
        
        
        for x in payment_history:

            dynamic_amt += x.amount_paid
            cur_balance = calc_balance(dynamic_amt, h.float2decimal(vat_total))

            tmp = {}

            tmp["date_created"] = x.date_created.strftime("%Y-%m-%d")
            tmp["amount_paid"] = x.amount_paid
         
            payment_agg.append(tmp)
        if request.method == 'GET':
            generate_pdf(_template='receipt.html', args=items, 
                         kwargs=data, email_body_template='email_receipt.html', 
                         pay_history=payment_agg)
            

            msg = "Receipt has been emailed to the Customer successfully."
            return redirect(url_for('payment.index', msg=msg))



