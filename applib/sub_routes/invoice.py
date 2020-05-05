
import os
import subprocess
import pdfkit
import base64
import datetime


from flask import (Blueprint, request, url_for, 
                   render_template, redirect, session, flash)
 

from jinja2 import Template
from jinja2 import Environment, PackageLoader, FileSystemLoader
import random 


# from applib.model import db_session
from applib import model as m 
from applib.forms import CreateInvoiceForm

from applib.lib import helper as h 
from applib.lib.helper import (get_config, send_email, calc_discount, 
                        set_email_read_feedback, generate_pdf, comma_separation,
                        set_pagination)


from flask_login import login_required

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

mod = Blueprint('invoice', __name__, url_prefix='/admin/invoice')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@mod.route('/')
@login_required
def index():

    posts=[]
    cur_page = request.args.get('page', 1, int)

    with m.sql_cursor() as db:
        #select query from invoice
        sub = db.query(m.Items.invoice_id,
                       m.func.sum(m.Items.amount                                              
                                  ).label("sub_total"),
                       ).group_by(
                            m.Items.invoice_id
                       ).subquery()


        recent_payments = db.query(m.Payment.invoice_id, 
                                  m.func.max(m.Payment.status).label('status'),
                                   m.func.sum(m.Payment.amount_paid).label('recent_payment')
                                  ).group_by(m.Payment.invoice_id).subquery()

        qry = db.query(m.Invoice.inv_id, 
                       m.Invoice.invoice_no, m.Invoice.disc_type, m.Invoice.disc_value,
                       m.Invoice.client_type, m.Client.email, 
                       m.Client.name, m.Invoice.date_value,
                       # m.Payment.status,                      
                       sub.c.sub_total,
                       sub.c.invoice_id,
                       recent_payments.c.recent_payment,
                       recent_payments.c.status
                      ).outerjoin(sub, sub.c.invoice_id == m.Invoice.inv_id
                      # ).outerjoin(m.Payment, 
                      #             m.Payment.invoice_id == m.Invoice.inv_id
                      ).outerjoin(recent_payments, 
                                  recent_payments.c.invoice_id == m.Invoice.inv_id
                                  ).filter(m.Invoice.client_id == m.Client.id
                                           ).order_by(m.Invoice.inv_id.desc())
                                                        
        qry, page_row = set_pagination(qry, cur_page, 10)

        grp_data = []

       
        for x in qry.items:
            retv = {}

            retv['date_value'] = x.date_value 
            retv['inv_id'] = x.inv_id 
            retv['invoice_no'] = x.invoice_no
            retv['client_name'] = x.name
            retv['email'] = x.email

            vat_total, vat, total, discount = h.val_calculated_data(x.disc_type, x.disc_value, 
                                                                    x.sub_total, x.client_type)
            retv['status'] = x.status
            # retv['status'] = 1 if ((x.recent_payment or 0) - h.float2decimal(vat_total)) == 0 else 2 

            retv['vat_total'] = vat_total
            retv['vat'] = vat 
            retv['total'] = total
            retv['discount'] = discount 

            grp_data.append(retv)


        cur_fmt = comma_separation

                                  
    msg = request.args.get('msg')
    if msg:
        flash(msg)

    return render_template('index.html',
                            pager=qry, page_row=page_row, data=grp_data, 
                            cur_page=cur_page, cur_fmt=cur_fmt, )



@mod.route('/checkout/<int:invoice_id>', methods=['POST', 'GET'])
@login_required
def checkout(invoice_id):

    form = CreateInvoiceForm()
    currency_label = {x[0]: x[1] for x in form.currency.choices}
    
    with m.sql_cursor() as db:
        
        client_invoice_details = db.query(
                                           m.Invoice.inv_id,
                                           m.Invoice.date_value,
                                           m.Invoice.invoice_no,
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
                                               m.Payment.invoice_id == m.Invoice.inv_id
                                        ).filter(
                                                m.Invoice.inv_id == invoice_id
                                            ).first()

        item_for_amount = db.query(m.Items.id, m.Items.item_desc,
                                   m.Items.qty, m.Items.rate,
                                   m.Items.amount
                                  ).filter_by(invoice_id=invoice_id).all()

        data = {
                'invoice_no': client_invoice_details.invoice_no,
                'date_value': datetime.datetime.now().strftime("%Y-%m-%d"),
                'invoice_due': datetime.datetime.now().strftime("%Y-%m-%d"),
                'purchase_order_no': client_invoice_details.purchase_no,
                'discount_applied': client_invoice_details.disc_value,
                'discount_description': client_invoice_details.disc_desc,
                'address': client_invoice_details.address,
                'post_addr': client_invoice_details.post_addr,
                'name': client_invoice_details.name,
                'disc_type': client_invoice_details.disc_type,
                'email': client_invoice_details.email,
                'phone': client_invoice_details.phone,
                'currency': currency_label[client_invoice_details.currency],
                'status': client_invoice_details.status,
                }

        data['cur_fmt'] = comma_separation

        _amount = 0

        for x in item_for_amount:
            _amount += x.amount

        data['subtotal'] = _amount
        vat_total, vat, total, discount = h.val_calculated_data(client_invoice_details.disc_type, 
                                                              client_invoice_details.disc_value, 
                                                              _amount, client_invoice_details.client_type)

        data['discount'] = discount
        data['vat'] = vat
        data['total'] = total
        data['vat_total'] = vat_total

        if request.method == 'POST':

            items = []
            for y in item_for_amount:
                items.append({
                                'id': y.id, 'item_desc': y.item_desc,
                                'qty': y.qty, 'rate': y.rate, 'amount': y.amount
                              })

            data['type'] = "Invoice"
            generate_pdf(_template='new_invoice.html', args=items, 
                        kwargs=data, email_body_template='email_body.html')
            
            msg = "Invoice has been emailed to the customer successfully."
            return redirect(url_for('invoice.index', msg=msg))


        # render the page on GET 
        return render_template('checkout.html', 
                                invoice_details=client_invoice_details,
                                client_details=client_invoice_details, 
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

        if request.method == 'POST' and form.validate():
     
            invoice = m.Invoice()
            m.form2model(form, invoice)
            invoice.date_value = datetime.datetime.now()
            invoice.invoice_due = datetime.datetime.now()
            db.add(invoice)
            db.flush()
            invoice.invoice_no = 'INV-%d' %invoice.inv_id
            invoice.purchase_no = invoice.inv_id

            return redirect(url_for('item.add_item', invoice_id=invoice.inv_id))

    return render_template('client_invoice.html', form=form)

