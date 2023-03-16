# +-------------------------+-----------------------------+
# Written By   : Uzodinma Jeff
# +-------------------------+-----------------------------+
# Filename     : 
# +-------------------------+-----------------------------+
# Description  :
#              :
# +-------------------------+-----------------------------+
# Company Name :  Ecardex Ltd 
# +-------------------------+-----------------------------+


from flask import (Blueprint, request, url_for, 
                   render_template, redirect, session, flash)
from flask_login import login_required

import datetime, calendar


from applib import model as m 
from applib.lib import helper as h

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

mod = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

def get_year_range(year):

    dt = datetime.datetime.now()
    rng = calendar.monthrange(year, dt.month)

    start = datetime.datetime(year, 1, 1,hour=0, minute=0, second=0)
    end = datetime.datetime(year, dt.month, rng[1],hour=23, minute=59, second=59)

    return start, end


@mod.route('/')
@login_required
def index():

    nt = datetime.datetime.now()
 
    yr = request.args.get('year', nt.year, int)
    nt = nt.replace(year=yr)

    with m.sql_cursor() as db:
 
        
        qry = db.query(
                m.func.extract('MONTH', m.Payment.date_created).label('month'),
                m.func.sum(m.Payment.amount_paid)
            ).filter(
                m.func.extract('YEAR', m.Payment.date_created) == nt.year #strftime('%Y-%m')
                
            ).group_by(
                m.func.extract('MONTH', m.Payment.date_created).label('month')
            )

        
        cur_income = qry.filter(
                        m.func.extract('MONTH', m.Payment.date_created) == nt.month
                    ).all()

        annual_income = qry.all()


        qry2 = db.query(
                    m.func.extract('MONTH', m.Expense.date_created),
                    m.func.sum(m.Expense.amount)
                ).filter(
                    m.func.extract('YEAR', m.Expense.date_created) == nt.year
                ).group_by(
                    m.func.extract('MONTH', m.Expense.date_created).label('month')
                )
        
        cur_exp = qry2.filter(
                    m.func.extract('MONTH', m.Expense.date_created) == nt.month
                ).all()

        annual_exp = qry2.all()

 
        start, _stop = get_year_range(yr)

        items_sub = db.query(
            m.Invoice.inv_id,
            m.func.sum(m.Items.amount).label("total_amount")
        ).join(
            m.Items,
            m.Items.invoice_id == m.Invoice.inv_id          
        ).filter(
            m.Invoice.date_value.between(start, _stop)
        ).group_by(m.Invoice.inv_id).subquery()

        payment_sub = db.query(
            m.Payment.invoice_id,
            m.func.sum(m.Payment.amount_paid).label("total_paid")
        ).filter(
            m.Payment.date_created.between(start, _stop)
        ).group_by(
            m.Payment.invoice_id
        ).subquery()

        invoices_data = db.query(
            m.Invoice.inv_id,
            m.Invoice.client_type,
            m.Invoice.disc_type,
            m.Invoice.disc_value,
            items_sub.c.total_amount,
            payment_sub.c.total_paid        
        ).join(
            items_sub, items_sub.c.inv_id == m.Invoice.inv_id
        ).outerjoin(
            payment_sub,
            payment_sub.c.invoice_id == m.Invoice.inv_id
        ).filter(
            m.Invoice.date_value.between(start, _stop)
        ).all()


    debt = h.float2decimal("0")

    for x in invoices_data:
        
        if x.total_paid:
            overall_total = h.val_calculated_data(x.disc_type, x.disc_value, x.total_amount, x.client_type)
            tmp = h.float2decimal(overall_total[0]) - x.total_paid

            if tmp > 0:
                debt += tmp

    tmp_inc = {int(x): k for x,k in annual_income}

    tmp_exp = {int(x): k for x,k in annual_exp}

    income_aggregate, exp_aggregate = h.float2decimal('0'), h.float2decimal('0')

    for x,k in annual_income:
        income_aggregate += k 

    for x,k in annual_exp :
        exp_aggregate += k 
 

    inc_output, exp_output = [], []
    
    for x in range(1,13):
        
        if x in tmp_inc.keys():
            inc_output.append(int(tmp_inc[x]))
        else:
            inc_output.append(0)

        if x in tmp_exp.keys():
            exp_output.append(int(tmp_exp[x]))
        else:
            exp_output.append(0)


    cur_income_value = 0 
    cur_exp_value = 0

    if cur_income:
        cur_income_value = int(cur_income[0][1])
    
    if cur_exp:
        cur_exp_value = int(cur_exp[0][1])

    return render_template("dashboard.html", 
                           inc_output=inc_output, 
                           exp_output=exp_output,                          
                           cur_month=nt.strftime('%B'),
                           cur_income_val=cur_income_value,
                           cur_exp_val=cur_exp_value,
                           debt_val=debt, year=yr,
                           aggregate=[income_aggregate,exp_aggregate]
                          )

