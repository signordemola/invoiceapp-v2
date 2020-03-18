
from flask import (Blueprint, request, url_for, 
				   render_template, redirect, session, flash)

import applib.model as m
from applib.forms import PaymentForm, CreateInvoiceForm
from applib.lib import helper as h 
from applib.lib.helper import (get_config, send_email, calc_discount,
								set_email_read_feedback, generate_pdf, 
								comma_separation, set_pagination)

from flask_login import login_required

import os
import subprocess
import pdfkit
import base64
import datetime

from jinja2 import Template
from jinja2 import Environment, PackageLoader, FileSystemLoader
import random


mod = Blueprint('payment', __name__, url_prefix='/admin/payment')

@mod.route("/")
@login_required
def index():
	form = PaymentForm(request.form)
	status = { x[0]: x[1] for x in form.status.choices}
	cur_page = request.args.get('page', 1, int)


	with m.sql_cursor() as db:
		qry = db.query(m.Payment.id,
					   m.Payment.payment_desc,
					   m.Payment.date_created,
					   m.Payment.payment_mode,
					   m.Payment.amount_paid,
					   m.Payment.balance,
					   m.Payment.invoice_id,
					   m.Payment.status,
					   m.Client.name,
					   m.Invoice.inv_id.label("inv_id"),
					  ).join(m.Invoice,
							 m.Invoice.inv_id == m.Payment.invoice_id
							 ).join(m.Client,
									m.Client.id == m.Invoice.client_id
									).filter(m.Payment.invoice_id == m.Invoice.inv_id
									).order_by(m.Invoice.inv_id.desc())
		
		qry, page_row = set_pagination(qry, cur_page)

		cur_fmt = comma_separation									


	msg = request.args.get("msg")
	if msg:
		flash(msg)


	return render_template('payment.html', data=qry, status_label=status,
							date_format=h.date_format, pager=qry, 
							page_row=page_row, cur_page=cur_page, 
							cur_fmt=cur_fmt
						   )


@mod.route("/add/<int:invoice_id>/<invoice_name>", methods=["POST", "GET"])
@login_required
def add(invoice_name, invoice_id):
	form = PaymentForm(request.form, client_name=invoice_name)
	form_inv = CreateInvoiceForm()
	currency_label = {x[0]: x[1] for x in form_inv.currency.choices} 
	
	with m.sql_cursor() as db:
		item_details = db.query(m.Items.amount, m.Items.item_desc).filter_by(
														invoice_id=invoice_id
														).all()
		invoice_query = db.query(m.Invoice.inv_id,
								 m.Invoice.disc_type, 
								 m.Invoice.disc_value,
								 m.Invoice.client_type,
								 m.Invoice.currency).filter_by(inv_id=invoice_id
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
			pay_md.date_created = datetime.datetime.now().strftime("%b-%m-%d")
			db.add(pay_md)

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

	form = PaymentForm(request.form)
	payment_mode_label = {x[0]: x[1] for x in form.payment_mode.choices}
	status_label = {x[0]: x[1] for x in form.status.choices}

	form_inv = CreateInvoiceForm()
	currency_label = {x[0]: x[1] for x in form_inv.currency.choices}
	
	if request.method == 'POST' and form.validate():
		with m.sql_cursor() as db:
			pay_md = db.query(m.Payment).get(pay_id)
			m.form2model(form, pay_md)
		
		return redirect(url_for("payment.index", msg='Paymemt updated successfully.'))
			
	with m.sql_cursor() as db:

		item_details = db.query(m.Items.amount, 
								m.Items.item_desc
								).filter_by(
											invoice_id=invoice_id
											).all()

		invoice_query = db.query(m.Invoice.inv_id, 
								 m.Invoice.disc_type, 
								 m.Invoice.disc_value,
								 m.Invoice.client_type,
								 m.Invoice.currency,
								 m.Payment.date_created,
								 m.Payment.amount_paid,
								 m.Payment.payment_mode,
								 m.Payment.balance,
								 m.Payment.status
								 ).join(
										m.Payment, 
										m.Payment.invoice_id == m.Invoice.inv_id
								 ).filter(m.Invoice.inv_id == invoice_id).all()

		amount_sum = db.query(m.func.sum(m.Payment.amount_paid).label("amount_paid_sum"), 
							  m.Payment.invoice_id
							 ).join(
							  m.Invoice, 
							  m.Invoice.inv_id == m.Payment.invoice_id
							 ).filter(
							  m.Invoice.inv_id == invoice_id
							 ).group_by(m.Payment.invoice_id).first()

		_amount_sum = amount_sum.amount_paid_sum
		grp_data = []


		for x in invoice_query:
			retv = {}

			retv['date_created'] = x.date_created.strftime("%d-%m-%Y")
			retv['amount_paid'] = x.amount_paid
			retv['payment_mode'] = payment_mode_label[x.payment_mode]
			retv['balance'] = x.balance
			retv['status'] = status_label[x.status]

			grp_data.append(retv)

		data = {}

		_amount = 0
		for x in item_details:
			_amount += x.amount

		vat_total, vat, total, discount = h.val_calculated_data(invoice_query[0].disc_type, 
																invoice_query[0].disc_value, 
																_amount, 
																invoice_query[0].client_type)

		data['cur_fmt'] = comma_separation
		data['currency'] = currency_label[invoice_query[0].currency]    
		pay_data = db.query(m.Payment.id,
							m.Client.name.label('client_name'),
							# m.Payment.payment_desc,
							m.Payment.client_name,
							# m.Payment.payment_mode,
							# m.Payment.amount_paid,
							m.Payment.balance,
							# m.Payment.status
							).join(
							m.Invoice,
							m.Invoice.inv_id == m.Payment.invoice_id
							).join(
							m.Client, m.Client.id == m.Invoice.client_id
							).filter(m.Payment.id == pay_id).first()

		

		m.model2form(pay_data, form)

	return render_template("edit_payment.html", 
							form=form, 
							title="Add Payment",
							discount=discount,
							total=vat_total,
							subtotal=total,
							amount_sum=_amount_sum,
							vat=vat,
							item_details=item_details,
							kwargs=data,
							grp_data=grp_data)



@mod.route("/receipt/<int:invoice_id>", methods=['POST', 'GET'])
@login_required
def receipt(invoice_id):

	form_pay = PaymentForm()
	status = {x[0]: x[1] for x in form_pay.status.choices}

	form_inv = CreateInvoiceForm()
	currency_label = {x[0]: x[1] for x in form_inv.currency.choices}

	with m.sql_cursor() as db:
		client_invoice_details = db.query(m.Invoice.inv_id.label("invoice_id"),
										  m.Invoice.invoice_no, m.Invoice.disc_value,
										  m.Invoice.disc_type, m.Invoice.currency,
										  m.Invoice.client_type,
										  m.Payment.amount_paid, m.Payment.status, 
										  m.Payment.date_created,
										  m.Payment.balance, m.Client.address,
										  m.Client.post_addr, m.Client.name,
										  m.Client.email, m.Client.phone
										).join(m.Invoice,
											   m.Invoice.inv_id == m.Payment.invoice_id
										).join(m.Client,
											   m.Client.id == m.Invoice.client_id
											   ).filter(
													m.Payment.invoice_id == invoice_id
													).first()

		data = {
				'invoice_no': client_invoice_details.invoice_no,
				'date_value': client_invoice_details.date_created.strftime("%Y-%m-%d"),
				'address': client_invoice_details.address,
				'post_addr': client_invoice_details.post_addr,
				'name': client_invoice_details.name,
				'email': client_invoice_details.email,
				'phone': client_invoice_details.phone
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


		data['type'] = "Receipt"
		data['amount_balance'] = client_invoice_details.balance
		data['amount_paid'] = client_invoice_details.amount_paid

		vat_total, vat, total, discount = h.val_calculated_data(client_invoice_details.disc_type, 
																client_invoice_details.disc_value, 
																_amount, 
																client_invoice_details.client_type)

		data['subtotal'] = total
		data['vat'] = vat
		data['total'] = vat_total
		data['status'] = status[client_invoice_details.status]
		data['currency'] = currency_label[client_invoice_details.currency]


		if request.method == 'GET':
			generate_pdf(_template='receipt.html', args=items, 
						 kwargs=data, email_body_template='email_receipt.html')
			

			msg = "Receipt has been emailed to the Customer successfully."
			return redirect(url_for('payment.index', msg=msg))



