import os
import json
from applib import model as m
from applib.lib.helper import (
    get_current_timezone,
    comma_separation,
    val_calculated_data,
    generate_pdf,
    generate_html_template,
    send_email,
    float2decimal,
    figure2decimal
)



def notifications():
    print(f"[{get_current_timezone().strftime('%Y-%m-%d %H:%M:%S')}] Starting invoice reminder process...")

    current_date = get_current_timezone().date()

    all_invoice_data = []

    with m.sql_cursor() as session_db:
        all_invoice_data = session_db.query(
            m.Invoice.id.label('invoice_id'),
            m.Invoice.invoice_no.label('invoice_no'),
            m.Invoice.date_value.label('invoice_date_value'),
            m.Invoice.invoice_due.label('invoice_due'),
            m.Invoice.send_reminders.label('send_reminders'),
            m.Invoice.reminder_frequency.label('reminder_frequency'),
            m.Invoice.reminder_logs.label('reminder_logs'),
            m.Invoice.disc_type.label('disc_type'),
            m.Invoice.disc_value.label('disc_value'),
            m.Invoice.client_type.label('client_type'),
            m.Client.name.label('client_name'),
            m.Client.email.label('client_email'),
            m.Items.id.label('item_id'),
            m.Items.item_desc.label('item_desc'),
            m.Items.qty.label('item_qty'),
            m.Items.rate.label('item_rate'),
            m.Items.amount.label('item_amount'),
            m.Payment.id.label('payment_id'),
            m.Payment.amount_paid.label('payment_amount_paid'),
            m.Payment.status.label('payment_status'),
            m.Payment.balance.label('payment_balance'),
            m.Payment.date_created.label('payment_date_created')
        ).join(
            m.Client, m.Client.id == m.Invoice.client_id
        ).join(
            m.Items, m.Items.invoice_id == m.Invoice.id
        ).outerjoin(
            m.Payment, m.Payment.invoice_id == m.Invoice.id
        ).filter(
            m.Invoice.send_reminders.is_(True)
        ).order_by(
            m.Invoice.id
        ).all()

    if not all_invoice_data:
            print("No invoices found with 'send_reminders' enabled. Exiting.")
            return

    invoices_grouped = {}
    for row in all_invoice_data:
        invoice_id = row.invoice_id

        if invoice_id not in invoices_grouped:
            reminder_logs_parsed = []
            if row.reminder_logs:
                try:
                    reminder_logs_parsed = json.loads(row.reminder_logs)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode reminder_logs for invoice {invoice_id}: {row.reminder_logs}")
                    reminder_logs_parsed = []

            invoices_grouped[invoice_id] = {
                'id': row.invoice_id,
                'invoice_no': row.invoice_no,
                'date_value': row.invoice_date_value,
                'invoice_due': row.invoice_due,
                'send_reminders': row.send_reminders,
                'reminder_frequency': row.reminder_frequency,
                'reminder_logs': reminder_logs_parsed,
                'disc_type': row.disc_type,
                'disc_value': row.disc_value,
                'client_type': row.client_type,
                'client_name': row.client_name,
                'client_email': row.client_email,
                'items': [],
                'payments': [],
                'processed_item_ids': set(),
                'processed_payment_ids': set()
            }

        if row.item_id is not None and row.item_id not in invoices_grouped[invoice_id]['processed_item_ids']:
            invoices_grouped[invoice_id]['items'].append({
                'item_id': row.item_id,
                'item_desc': row.item_desc,
                'qty': row.item_qty,
                'rate': row.item_rate,
                'amount': row.item_amount
            })
            invoices_grouped[invoice_id]['processed_item_ids'].add(row.item_id)

        if row.payment_id is not None and row.payment_id not in invoices_grouped[invoice_id]['processed_payment_ids']:
            invoices_grouped[invoice_id]['payments'].append({
                'payment_id': row.payment_id,
                'amount_paid': row.payment_amount_paid,
                'status': row.payment_status,
                'balance_at_payment': row.payment_balance,
                'date_created': row.payment_date_created.strftime('%Y-%m-%d %H:%M:%S') if row.payment_date_created else None
            })
            invoices_grouped[invoice_id]['processed_payment_ids'].add(row.payment_id)


    invoices_to_process = list(invoices_grouped.values())

    invoices_to_process.sort(key=lambda x: x['invoice_no'])

    zero = figure2decimal('0')

    for invoice_data_dict in invoices_to_process:
        invoice_id = invoice_data_dict['id']
        invoice_no = invoice_data_dict['invoice_no']
        date_value = invoice_data_dict['date_value']
        invoice_due = invoice_data_dict['invoice_due']
        send_reminders = invoice_data_dict['send_reminders']
        reminder_frequency = invoice_data_dict['reminder_frequency']
        reminder_logs = invoice_data_dict['reminder_logs']

        disc_type = invoice_data_dict['disc_type']
        disc_value = invoice_data_dict['disc_value']
        client_type = invoice_data_dict['client_type']
        client_name = invoice_data_dict['client_name']
        client_email = invoice_data_dict['client_email']
        items = invoice_data_dict['items']
        payments = invoice_data_dict['payments']

        invoice_subtotal = sum(item['amount'] for item in items) if items else zero

        invoice_total_after_calc_float, vat_amount, total_after_discount, discount_amount = val_calculated_data(
            disc_type,
            disc_value,
            invoice_subtotal,
            client_type
        )

        invoice_total_after_calc = float2decimal(invoice_total_after_calc_float)
        amount_paid_for_invoice = sum(payment['amount_paid'] for payment in payments) if payments else zero
        outstanding_balance = invoice_total_after_calc - amount_paid_for_invoice

        if outstanding_balance > zero:
            email_data = {
                'client_name': client_name,
                'client_email': client_email,
                'invoice_no': invoice_no,
                'invoice_id': invoice_id,
                'date_value': date_value.strftime('%Y-%m-%d'),
                'invoice_due': invoice_due.strftime('%Y-%m-%d'),
                'balance': outstanding_balance,
                'subtotal': invoice_subtotal,
                'total': invoice_total_after_calc,
                'amount_paid_for_invoice': amount_paid_for_invoice,
                'items': [{
                    'item_desc': item['item_desc'],
                    'qty': item['qty'],
                    'rate': item['rate'],
                    'amount': item['amount']
                } for item in items],
                'payments': [{
                    'amount_paid': payment['amount_paid'],
                    'status': payment['status'],
                    'balance_at_payment': payment['balance_at_payment'],
                    # 'date_created': payment['date_created'].strftime('%Y-%m-%d %H:%M:%S') if payment['date_created'] else None
                } for payment in payments],
                'disc_type': disc_type,
                'disc_value': disc_value,
                'client_type': client_type,
                'discount': discount_amount,
                'vat': vat_amount,
                'vat_total': invoice_total_after_calc,
                'paid_to_date': amount_paid_for_invoice,
                'currency': '&#8358;',
                'cur_fmt': comma_separation,
                'type': 'Invoice'
            }

            pdf_path = generate_pdf(
                _template='new_invoice.html',
                args=email_data['items'],
                kwargs=email_data,
                email_body_template='email_body.html',
                isdownload=True,
                send_email=False
            )

            email_subject = f"Reminder: Invoice #{invoice_no} - {comma_separation(outstanding_balance)} Due"
            email_body_html = generate_html_template(
                folder='applib/templates',
                template='email_body.html',
                invoice_data=email_data,
            )

            send_email(
                filename=pdf_path,
                receiver_email='jeffrey@ecardex.com',
                msg_subject=email_subject,
                email_body=email_body_html,
                email_filename=f'Reminder {invoice_no}'
            )

            if pdf_path and os.path.isfile(pdf_path):
                os.remove(pdf_path)
                print(f"Deleted PDF after sending: {pdf_path}")

        else:
            print(
                f"--- Invoice: {invoice_no} (ID: {invoice_id}) --- No outstanding balance. Skipping email_data preparation.")
            print("--------------------------------------------------")

    print(f"[{get_current_timezone().strftime('%Y-%m-%d %H:%M:%S')}] Invoice reminder process completed.")



if __name__ == '__main__':
    notifications()
