
import os
import subprocess
import pdfkit
import base64
import datetime


from sqlalchemy import update 

from flask import (Blueprint, request, url_for, send_file,
                   render_template, redirect, flash)

from applib import model as m
from applib.forms import CreateInvoiceForm

from applib.lib import helper as h
from applib.lib.helper import (
    generate_pdf, 
    get_current_timezone,
    comma_separation,
    set_pagination)


from flask_login import login_required

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

mod = Blueprint('invoice', __name__, url_prefix='/invoice')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@mod.route('/')
@login_required
def index():

    posts=[]
    cur_page = request.args.get('page', 1, int)
    search = request.args.get('search', "")

    with m.sql_cursor() as db:
         
        sub = db.query(
                m.Items.invoice_id,
                m.func.sum(m.Items.amount).label("sub_total"),
            ).group_by(
                m.Items.invoice_id
            ).subquery()

        recent_payments = db.query(
                m.Payment.invoice_id,
                m.func.max(m.Payment.status).label('status'),
                m.func.sum(m.Payment.amount_paid).label('recent_payment')
           ).group_by(m.Payment.invoice_id).subquery()

        qry = db.query(m.Invoice.id,
                       m.Invoice.invoice_no, m.Invoice.disc_type, 
                       m.Invoice.disc_value,
                       m.Invoice.client_type, 
                       m.Client.email,
                       m.Client.name, m.Invoice.date_value,  
                       sub.c.sub_total,
                       recent_payments.c.recent_payment,
                       recent_payments.c.status
                    ).outerjoin(
                        sub, sub.c.invoice_id == m.Invoice.id
                    ).outerjoin(recent_payments,
                                recent_payments.c.invoice_id == m.Invoice.id
                    ).filter(
                        m.Invoice.client_id == m.Client.id
                    ).order_by(m.Invoice.id.desc())


        if search:
             
            qry = qry.filter(
                    m.or_(
                        m.Client.name.like(f'%{search}%'),
                        m.Client.email.like(f"%{search}%")
                    )
                )
        qry, page_row = set_pagination(qry, cur_page, 10)

        grp_data = []
 
        for x in qry.items:
            retv = {}
            retv['date_value'] = x.date_value
            retv['inv_id'] = x.id
            retv['invoice_no'] = x.invoice_no
            retv['client_name'] = x.name
            retv['email'] = x.email

            vat_total, vat, total, discount = h.val_calculated_data(x.disc_type, x.disc_value,
                                                                    x.sub_total or 0, x.client_type)
            retv['status'] = x.status
            retv['vat_total'] = vat_total
            retv['vat'] = vat
            retv['total'] = total
            retv['discount'] = discount

            grp_data.append(retv)

        cur_fmt = comma_separation


    msg = request.args.get('msg')
    if msg:
        flash(msg)

    return render_template('invoice_list.html',
                            pager=qry, page_row=page_row, data=grp_data,
                            cur_page=cur_page, cur_fmt=cur_fmt
                        )

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@mod.route('/checkout/<int:invoice_id>', methods=['POST', 'GET'])
@login_required
def checkout(invoice_id):

    form = CreateInvoiceForm()
    currency_label = {x[0]: x[1] for x in form.currency.choices}


    with m.sql_cursor() as db:

        invoice_data = db.query(
                        m.Invoice.id,
                        m.Invoice.date_value,
                        m.Invoice.invoice_no,
                        m.Invoice.invoice_due,
                        m.Invoice.purchase_no,
                        m.Invoice.disc_value,
                        m.Invoice.disc_type,
                        m.Invoice.disc_desc,
                        m.Invoice.currency,
                        m.Invoice.client_type,
                        m.Payment.status,
                        m.Payment.id.label("pay_id"),
                        m.Client.address,
                        m.Client.post_addr,
                        m.Client.name,
                        m.Client.email,
                        m.Client.phone,
                        m.Client.id.label('client_id')
                    ).join(
                            m.Client,
                            m.Client.id == m.Invoice.client_id
                    ).outerjoin(
                            m.Payment,
                            m.Payment.invoice_id == m.Invoice.id
                    ).filter(
                            m.Invoice.id == invoice_id
                    ).first()

        item_for_amount = db.query(m.Items.id, m.Items.item_desc,
                                   m.Items.qty, m.Items.rate,
                                   m.Items.amount
                                  ).filter_by(invoice_id=invoice_id).all()

    
    data = {
            'invoice_no': invoice_data.invoice_no,
            'date_value': invoice_data.date_value.strftime("%Y-%m-%d"),
            'invoice_due': invoice_data.invoice_due.strftime("%Y-%m-%d"),
            'purchase_order_no': invoice_data.purchase_no,
            'discount_applied': invoice_data.disc_value,
            'discount_description': invoice_data.disc_desc,
            'address': invoice_data.address,
            'post_addr': invoice_data.post_addr,
            'name': invoice_data.name,
            'disc_type': invoice_data.disc_type,
            'email': invoice_data.email,
            'phone': invoice_data.phone,
            'currency': currency_label[invoice_data.currency],
            'status': invoice_data.status,
            }

    data['cur_fmt'] = comma_separation

    _amount = 0

    for x in item_for_amount:
        _amount += x.amount

    data['subtotal'] = _amount
    vat_total, vat, total, discount = h.val_calculated_data(invoice_data.disc_type,
                                                          invoice_data.disc_value,
                                                          _amount, invoice_data.client_type)

    data['discount'] = discount
    data['vat'] = vat
    data['total'] = total
    data['vat_total'] = vat_total

    download = request.args.get("download", 0, int)

    if request.method == 'POST' or download == 1:
        
        items = []
        for y in item_for_amount:
            items.append({
                            'id': y.id, 'item_desc': y.item_desc,
                            'qty': y.qty, 'rate': y.rate, 'amount': y.amount
                          })


        
        data['type'] = "Invoice"
        
        if download == 1:
            pdf_file = generate_pdf(_template='new_invoice.html', args=items,
                    kwargs=data, email_body_template='email_body.html', isdownload=True)

            return send_file(os.path.join(os.getcwd(), pdf_file))

        generate_pdf(_template='new_invoice.html', args=items,
                    kwargs=data, email_body_template='email_body.html')

        msg = "Invoice has been emailed to the customer successfully."
        return redirect(url_for('invoice.index', msg=msg))



    # render the page on GET
    return render_template('checkout.html',
                            invid=invoice_id,
                            invoice_details=invoice_data,
                            client_details=invoice_data,
                            kwargs=data,
                            items=item_for_amount)


@mod.route('/add', methods=['POST', 'GET'])
@login_required
def client_invoice():

    form = CreateInvoiceForm(request.form)
    form.client_id.choices = [(0, 'Select a User...')]

    with m.sql_cursor() as db:
        qry = db.query(m.Client).order_by(m.Client.id.desc()).all()
        form.client_id.choices.extend([(g.id, g.name) for g in qry])


        empty_bill = db.query(m.RecurrentBill.id, m.RecurrentBill.product_name
                ).filter(m.RecurrentBill.invoice_id.is_(None)).all()
        form.bill_id.choices += empty_bill


        if request.method == 'POST' and form.validate():

            invoice = m.Invoice()
            m.form2model(form, invoice)

            bill_data = None
            if form.bill_id.data is not None:

                bill_data = db.query(m.RecurrentBill.date_due
                        ).filter(m.RecurrentBill.id == form.bill_id.data).first()


            invoice.date_value = datetime.datetime.now()
            invoice.invoice_due = bill_data.date_due if bill_data else datetime.datetime.now()
            db.add(invoice)
            db.flush()
            invoice.invoice_no = 'INV-%d' %invoice.id
            invoice.purchase_no = invoice.id


            if bill_data is not None:
                db.execute(
                    update(m.RecurrentBill)
                    .where(m.RecurrentBill.id == form.bill_id.data)
                    .values({'invoice_id': invoice.id, 'date_updated': get_current_timezone()})
                )


            return redirect(url_for('item.add_item', invoice_id=invoice.id))



    return render_template('client_invoice.html', form=form)
