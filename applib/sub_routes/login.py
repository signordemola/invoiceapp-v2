import datetime
import json

from flask import (Blueprint, request, url_for, render_template, redirect, session, flash, current_app)

from werkzeug.security import check_password_hash
from sqlalchemy import update

from applib.forms import LoginForm

from applib import model as m
from applib.lib.helper import decode_param, send_email

from flask_login import login_user, login_required, logout_user

mod = Blueprint('login', __name__)


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@mod.route('/', methods=['POST', 'GET'])
@mod.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)

    error = None

    if request.method == 'POST' and form.validate():
        username = form.usr_name.data
        password = form.psd_wrd.data


        print("\nLOGIN ATTEMPT:")
        print("Username:", username)
        print("Password submitted:", password)

        with m.sql_cursor() as db:

            user = db.query(m.Users).filter(m.Users.username == username).first()

            if user is None:
                error = 'Username does not exist!'

            elif current_app.config['TESTING']:
                if user.password != password:
                    error = 'Incorrect Password!'

            elif not check_password_hash(user.password, password):
                error = 'Incorrect Password!'

            if error is None:
                session['user_id'] = user.id
                session.modified =True
                login_user(user)

                return redirect(url_for('invoice.index'))

            flash(error)

    return render_template('login.html', form=form)


@mod.route("/logout")
@login_required
def logout_app():
    logout_user()
    return redirect(url_for('login.login'))


@mod.route("/email_receipt")
def report_email_receipt():
    """
        ref contains the following values
            reference=12
            email_type='invoice | receipt | campaign | reminders'
            email_title='the subject of the email that was sent'
            email_body="the body of themail"
    """
    ref = request.args.get("ref")

    if ref:
        values = decode_param(ref)
        counter = 1
        with m.sql_cursor() as db:
            qry = db.query(m.EmailReceipt).filter_by(ref=ref)
            fetch_qry = qry.first()
            if fetch_qry:
                counter = fetch_qry.counter + 1
                db.execute(
                    update(m.EmailReceipt)
                    .where(m.EmailReceipt.id == fetch_qry.id)
                    .values({"counter": counter,
                             "last_received": datetime.datetime.now()})
                )

            else:
                em = m.EmailReceipt()
                em.ref = ref
                em.counter = 1
                em.last_received = datetime.datetime.now()
                em.body = json.dumps(values)
                db.add(em)

            if values.get('ref_type'):
                if values['ref_type'] == 'invoice':
                    db.execute(
                        update(m.Invoice)
                        .where(m.Invoice.id == values['ref_id'])
                        .values({'view_count': counter, 'last_view': datetime.datetime.now()})
                    )

                else:

                    db.execute(
                        update(m.Payment)
                        .where(m.Payment.id == values['ref_id'])
                        .values({'view_count': counter, 'last_view': datetime.datetime.now()})
                    )

        if counter <= 2:  # prevent multiple
            dt = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
            body = render_template('email_status.html', date_time=dt, counter=counter, **values)
            send_email(None, "support@ecardex.com", "Read Confirmation", body)

    return "OK"










