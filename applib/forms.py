from wtforms import Form, validators, Field
from wtforms.fields import (BooleanField, StringField, 
                            SubmitField, DateField, 
                            IntegerField, TextAreaField, SelectField,
                            HiddenField, DateTimeField,PasswordField, FloatField)
from wtforms.validators import input_required, Email, Length, ValidationError

from wtforms import form, validators, fields
from wtforms.form import Form



def input_required():

    def check_required(form, field):
        if not field.data:
            raise ValidationError("field is required.")

    return check_required



def length( min=3, max=25 ):

    def _length(form, field):

        _field = str(field.data)
        if len(_field) < min:
            raise ValidationError("Length of field must be greater than %d"%min)

        if len(_field) > max:
            raise ValidationError("Length of Field Exceeded")

    return _length



def check_inp_length():

    def validate_amount(form, field):
        try: 
            float(field.data)
        except Exception as e:
            raise ValidationError('valid input required.')

    return validate_amount


def check_sign():

    def negative(form, field):
        if not field.data:
            raise ValidationError("valid input required")
        if float(field.data) < 1:
            raise ValidationError("valid input required.")

    return negative

class CustomerForm(Form):
    name = StringField('name', [input_required()])
    address = StringField('address', [input_required()])
    email = StringField('email', [input_required(), Email()])
    phone = StringField('phone', [input_required()])
    postal_code = IntegerField('postal_code')


class ItemForm(Form):
    client_name = StringField('Client Name :', 
                                render_kw={"class_": "form-control", 
                                            "readonly": "readonly"})

    client_type = StringField('Client Type :', 
                                render_kw={"class_": "form-control", 
                                            "readonly": "readonly"})

    item_desc = TextAreaField('Description :', [input_required()], 
                                render_kw={"class_": "form-control", 
                                            "autocomplete": "new-password"})

    qty = IntegerField('Quantity :', [input_required(), check_sign()], 
                                render_kw={"class_": "form-control", 
                                            "autocomplete": "new-password"})

    rate = IntegerField('Rate :', [input_required(), check_sign()], 
                        render_kw={"class_": "form-control", 
                                   "autocomplete": "new-password"})
    
    amt = IntegerField('Amount :', 
                        render_kw={"class_": "form-control", 
                                   "readonly": "readonly"})


class DiscountFrm(Form):
    discount_type = SelectField('Discount Type :', 
                                choices=[('select', 'Select...'), 
                                         ('fixed', 'Fixed'), 
                                         ('percent', 'Percentage')], 
                                render_kw={"class_": "form-control", 
                                           "style": "margin-bottom : 10px"})

    discount = IntegerField('Discount Applied :', [length(min=1)], 
                            render_kw={"class_": "form-control", 
                                       "autocomplete": "off"})

    disc_amt = IntegerField('Discount Value :', 
                            render_kw={"class_": "form-control", 
                                       "readonly": "readonly"})

    sub_total = IntegerField('Sub-Total :', [check_inp_length()], 
                             render_kw={"class_": "form-control", 
                                        "readonly": "readonly"})

    new_total = IntegerField('New Total :', 
                             render_kw={"class_": "form-control", 
                                        "readonly": "readonly"})

    disc_desc = TextAreaField("Description", [], 
                             render_kw={"class_": "form-control",
                                    "autocomplete": "off"})


class CreateClientForm(Form):
    name = StringField('Name :', [input_required()], 
                                render_kw={"class_": "form-control", 
                                            "autocomplete": "new-password"})

    address = TextAreaField('Address :', [input_required()], 
                                render_kw={"class_": "form-control", 
                                            "autocomplete": "new-password"})

    email = StringField('Email :', [input_required(), Email()], 
                                render_kw={"class_": "form-control", 
                                            "autocomplete": "new-password"})

    phone = StringField('Phone Number :', [input_required(), length(), 
                                                check_inp_length()], 
                                render_kw={"class_": "form-control", 
                                            "autocomplete": "new-password"})

    post_addr = StringField('Postal-Address :', [input_required()], 
                                render_kw={"class_": "form-control"})



class CreateInvoiceForm(Form):
    client_id = SelectField('Client Name :', 
                                [input_required()], 
                                coerce=int, 
                                render_kw={ "class_": "js-single form-control",                                            
                                            "style": "margin-bottom : 10px"})

    client_type = SelectField('Client Type :', 
                                [input_required()], coerce=int, choices=[
                                            (0, 'Select a Class...'),
                                            (1, 'Student'), 
                                            (2, 'Individual'), 
                                            (3, 'Corporate')],
                                render_kw=  {"class_": "form-control", 
                                             "style": "margin-bottom : 10px"})

    currency = SelectField('Currency :', 
                                [input_required()],
                                coerce=int, 
                                choices=[(0, 'Select...'),
                                        (1, 'NGN'), 
                                        (2, 'USD'),
                                        (3, 'GHC'), 
                                        (4, 'EUR')], 
                                render_kw=  {"class_": "form-control", 
                                             "style": "margin-bottom : 10px"})

    
    bill_id = SelectField(
            'Recurrent Bill:', 
            [],
            coerce=int,
            choices=[(0, 'Select Bill')], 
            render_kw={
                "class_": "form-control js-single", 
                "style": "margin-bottom : 10px"
            }
        )

        

class BillsForm(Form):
    disc_type = StringField('disc_type', [input_required()])
    disc_value = IntegerField('disc_value')
    amtPaid = IntegerField('amtPaid', [input_required()])
    currency = StringField('cur', [input_required()])

    def validate_disc_type(form, field):

        if field.data not in ['fixed', 'percentage']:
            raise ValidationError('Invalid discount type specified')


class BillingFrm(Form):
    
    id = IntegerField('', default=0, render_kw={"class_": "form-control", 'type': 'hidden'}) 
    client_id = SelectField(
        'Client', [input_required()], coerce=int, choices=[(-1, 'Select Client')],
        render_kw={'class_': "js-single form-control",
                    "style": "margin-bottom : 10px"}
    )
    
    product_name = StringField('Product', [input_required()], render_kw={'class_': 'form-control'})
    amount_expected = StringField('Amount', [input_required()], render_kw={'class_': 'form-control'})
    date_due = DateField('Date Due', [input_required()], render_kw={'class_': 'form-control', 'type': 'date'})
    



class ExpenseForm(Form):

    field_id = HiddenField("ID", render_kw={"class_": "form-control"})
    # date_created = DateTimeField("Date Created", render_kw={"class_": "form-control"} )
    
    title = StringField("Title", [input_required()], 
                        render_kw={"class_": "form-control"})

    desc = TextAreaField("Description", [input_required()], 
                         render_kw={"class_": "form-control"})

    amount = StringField("Amount Required", [input_required()], 
                        render_kw={"class_": "form-control"})
    
    requested_by = StringField("Requested By", [input_required()], 
                               render_kw={"class_": "form-control"})
    
    status = SelectField("Status", [input_required()], coerce=int, 
                         choices=[(1, "Pending"), (2, "Approved"), (3, "Denied")], 
                         render_kw={"class_": "form-control"})
    payment_type = SelectField("Payment Type", [input_required()], coerce=int, 
                                choices=[(0, "Select Type"), (1, "Office Expenses"), 
                                         (2, 'Salary Payment'), (3, "Bonus Payout"), 
                                         (4, "Miscellenous"),(5, "Vat Remittance")
                                        ],
                                render_kw={"class_": "form-control"}
                               )

    aproved_by = StringField("Approved By", render_kw={"class_": "form-control"})
    
     

class PaymentForm(Form):

    client_name = StringField("Client Name", [input_required()],                            
                                render_kw={"class_": "js-single form-control",                                           
                                           "readonly": "readonly",
                                           "style": "margin-bottom : 10px"})

    payment_mode = SelectField("Mode Of Payment", [input_required()], 
                                coerce=int,
                                choices=[(0, "Select a Mode..."), 
                                        (1, "Cash"), (2, "Bank Transfer"),
                                        (3, "Online Merchant"), (4, "Cheque")],
                                render_kw={"class_": "form-control"})

    amount_paid = FloatField("Amount",
                                [input_required(), check_sign()], 
                                render_kw={"class_": "form-control",
                                           "autocomplete": "new-password"})

    balance = FloatField("Balance", 
                                render_kw={"class_": "form-control",
                                           "readonly": "readonly",
                                           "autocomplete": "new-password"})

    status = SelectField("Status", [input_required()], 
                                coerce=int, 
                                choices=[(1, "Complete"), (2, "Partial")], 
                                render_kw={"class_": "form-control"})

    payment_desc = TextAreaField('Comments', [input_required()], 
                                render_kw={"class_": "form-control", 
                                            "autocomplete": "new-password"})
        

class LoginForm(Form):

    usr_name = StringField("Username", [input_required()], 
                            render_kw={"class_": "form-control"})

    psd_wrd = PasswordField("Password", [input_required()],
                            render_kw={"class_": "form-control"})
         
 
 
 