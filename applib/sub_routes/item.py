
import os
import subprocess
import datetime

from sqlalchemy import update
from flask import (Blueprint, request, url_for, 
                   render_template, redirect, session, flash)


from applib.model import db_session
from applib import model as m 
from applib.forms import (ItemForm, DiscountFrm, CreateInvoiceForm)
from applib.lib.helper import calc_discount 

from applib.lib.helper import get_config 


from flask_login import login_required

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

mod = Blueprint('item', __name__, url_prefix='/item')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@mod.route('/item/<int:invoice_id>', methods=['POST', 'GET'])
@login_required
def add_item(invoice_id):

    client_label = { x[0]: x[1] for x in CreateInvoiceForm().client_type.choices}

    with m.sql_cursor() as db:
       
        client_param = db.query(m.Invoice.client_type,
                                m.Client.name
                                ).join(
                                        m.Client, 
                                        m.Client.id == m.Invoice.client_id 
                                       ).filter(
                                                m.Invoice.id == invoice_id 
                                                ).first()

        form = ItemForm(request.form, client_name=client_param.name, 
                        client_type=client_label[client_param.client_type]) 

    if request.method == 'POST' and form.validate():

        params={
                    'item_desc': form.item_desc.data,
                    'qty': form.qty.data,
                    'rate': form.rate.data,
                    'amount': form.amt.data
                }

        with m.sql_cursor() as db:

            params['invoice_id'] = invoice_id 

            # insert item query
            item = m.Items(**params)
            db.add(item)
            db.flush() 


            return redirect(url_for('invoice.checkout', invoice_id=invoice_id))


    return render_template('add_item.html', form=form)


@mod.route('/item/<int:invoice_id>/<int:item_id>', methods=['POST', 'GET'])
@login_required
def edit_item(invoice_id, item_id):

    with m.sql_cursor() as db:
        param = {'id': item_id}
        # select query with WHERE request
        resp = db.query(
                    m.Items.id,
                    m.Items.item_desc,
                    m.Items.qty,
                    m.Items.rate,
                    m.Items.amount,
                ).filter_by(**param)
       

        temp_resp = resp.first()
        client_param = db.query(
                        m.Invoice.client_type,
                        m.Client.name
                    ).join(
                        m.Client, 
                        m.Client.id == m.Invoice.client_id 
                    ).filter(
                        m.Invoice.id == invoice_id 
                    ).first()

        

        if request.method == 'POST':

            form = ItemForm(request.form)

            if form.validate():
                
                db.execute(                 
                    update(m.Items)
                    .where(m.Items.id == item_id)
                    .values(
                        {
                            'item_desc' : form.item_desc.data,
                            'qty' : form.qty.data,
                            'rate' : form.rate.data,
                            'amount' : form.amt.data                        
                        }
                    )
                )
              
                return redirect(url_for('invoice.checkout', invoice_id=invoice_id)) 


        form = ItemForm()
        form.client_name.data = client_param.name
        form.client_type.data = client_param.client_type
        form.item_desc.data = temp_resp.item_desc
        form.qty.data = temp_resp.qty 
        form.amt.data = temp_resp.amount


    return render_template('edit_item.html', form=form)


@mod.route('/delete/item/<int:invoice_id>/<int:item_id>')
@login_required
def delete_item(invoice_id, item_id):

    with m.sql_cursor() as db:
        param = {'id': item_id}
        # delete object query with WHERE request

        db.query(
                    m.Items                     
                ).filter_by(**param).delete()
        

        return redirect(url_for('invoice.checkout', invoice_id=invoice_id)) 



@mod.route('/discount/<int:invoice_id>', methods=['POST', 'GET'])
@login_required
def add_discount(invoice_id):

    with m.sql_cursor() as db:

        param = {'invoice_id': invoice_id}
 
        # select query with WHERE request
        resp = db.query(
                            m.Items.id,
                            m.Items.item_desc,
                            m.Items.qty,
                            m.Items.rate,
                            m.Items.amount,
                        ).filter_by(**param).all()

        resp_amount = 0

        if not resp:
            msg = "Please add an item to the invoice first."
            return redirect(url_for('invoice.index', msg=msg))

        # select query with WHERE request
        output = db.query(
                            m.Invoice.disc_value, 
                            m.Invoice.disc_type, 
                            m.Invoice.id
                          ).filter_by(id=invoice_id)

        temp_output = output.first()
         
        for x in resp:
            resp_amount += x.amount

        if temp_output.disc_type is None:
            form = DiscountFrm(sub_total=resp_amount)

        else:

            form = DiscountFrm()
            form.discount_type.data = temp_output.disc_type
            form.discount.data = temp_output.disc_value
            form.disc_amt.data = calc_discount(temp_output.disc_type, 
                                               temp_output.disc_value, 
                                               resp_amount)
            form.sub_total.data = resp_amount 
            form.new_total.data = resp_amount - form.disc_amt.data

         
        if request.method == 'POST':
            
            form = DiscountFrm(**request.form)
            
            if form.validate():

                assert resp_amount > 0 , 'total amount is not supposed to be zero amount'

                #sql update query
                db.execute(
                    update(m.Invoice)
                    .where(m.Invoice.id == invoice_id)
                    .values(
                        {
                            'disc_type' : form.discount_type.data,
                            'disc_value' : form.discount.data,
                            'disc_desc' : form.disc_desc.data,                     
                        }
                    )
                )
                
                return redirect(url_for('invoice.checkout', invoice_id=temp_output.id))        


        return render_template('disc.html', form=form)



@mod.route('/delete/discount/<int:invoice_id>')
@login_required
def delete_discount(invoice_id):

    with m.sql_cursor() as db:
        param = {'inv_id': invoice_id}
        # update object query with WHERE query

        resp = db.execute(

            update(
                m.Invoice 
            ).where(m.Invoice.id == invoice_id )
            .values(
                {
                    'disc_type' : None ,
                    'disc_value' : None ,
                    'disc_desc' : None,                       
                }
            )
        )
 
        return redirect(url_for('invoice.checkout', invoice_id=invoice_id)) 


