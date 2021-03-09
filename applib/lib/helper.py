
from configobj import ConfigObj

from passlib.hash import pbkdf2_sha256

from flask import url_for 

import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from jinja2 import Template
from jinja2 import Environment, PackageLoader, FileSystemLoader
import random 
import subprocess as sc 
import requests as rq 

import datetime, calendar
import urllib 
import base64

import os, json
import subprocess
import pdfkit
import base64
from sqlalchemy_pagination import paginate
from decimal import Decimal



# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


def get_config(header, key=None, filename='config.ini'):

    cfg = ConfigObj(filename)
    if not key:
        return cfg[header]

    return cfg[header][key]


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


class SetUri:
    """
        # default uri 
        # dialect+driver://username:password@host:port/database

        # default uri 
        # dialect+driver://username:password@host:port/database

        # postgresql uri structure 
        >>> postgresql://scott:tiger@localhost:5432/mydatabase 
        # sqlite uri structure 
        >>> sqlite:///foo.db

    """

    def __init__(self, db_cfg):
        self.db_cfg = db_cfg


    def set_credentials(self):
        tmp = self.db_cfg
        output = ''
        
        if tmp['username']:
            output = tmp['username'] + ':' + tmp["password"]

        return output


    def set_connections(self):
        
        output = ''

        if self.db_cfg['host']:
            output = '@'+ self.db_cfg['host'] + ':' + self.db_cfg['port']

        return output


    def set_db(self):        
        return  '/' + self.db_cfg['database']


    def set_driver(self):
        output = self.db_cfg['dialect'] 
        if self.db_cfg.get('driver', None):
            output += '+' + self.db_cfg['driver']

        output += '://'

        return output


    def run(self):
        
        return (self.set_driver() + self.set_credentials() 
                + self.set_connections() + self.set_db()
                )



def set_db_uri():

    _db_cfg = get_config('db')
    uri = SetUri(_db_cfg)
    return uri.run()

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


def encrypt_passwd(passwd):
    return pbkdf2_sha256.hash(passwd)


def validate_hash(passwd, hash):
    if not passwd or not hash:
        return False

    return pbkdf2_sha256.verify(passwd.encode('utf-8'), hash.encode('utf-8'))

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


def date_format(date_obj, strft='%H: %M: %S'):
    
    now = datetime.datetime.now()
    diff = now - date_obj

    if diff.days == 0:
        retv = date_obj.strftime(strft)

    elif diff.days == 1:
        retv = 'Yesterday'

    elif diff.days > 1 and diff.days < 10:
        retv = date_obj.strftime('%d, %B')

    else:
        retv = date_obj.strftime("%d-%m-%Y")
    

    return retv


def encode_param(**kwargs):        
    tmp = urllib.parse.urlencode(kwargs)
    params = base64.b64encode(tmp.encode('utf-8')).decode('utf-8')

    return params


def decode_param(value): 

    if isinstance(value, str):
        value = value.encode("utf-8")

    ret_val = base64.b64decode(value)
    ret_val = ret_val.decode("utf-8")

    out = {} 

    for x in ret_val.split("&"):
        key,val = x.split("=")
        out[key] = urllib.parse.unquote(val) 

    return out



def send_email(filename, receiver_email, msg_subject, 
               email_body, email_filename=""):
    
    email_params = get_config('email')

    if email_params['live'] == '1':

        body = email_body
        port = email_params['ssl']
        smtp_server =  email_params['smtp']
        password = email_params['passwd']
        sender_email = email_params['sender']
        message = MIMEMultipart()
        message["Subject"] = msg_subject
        message["From"] = email_params['sender']
        message["To"] = receiver_email

        message.attach(MIMEText(body, "html"))  #Add body to Email
        # filename = pdf_output  # In same directory as script

        attach_name = "{}.{}.pdf".format(email_filename, 
                                         datetime.datetime.now().strftime("%b.%m.%Y.%S"))
        
        attach_name = None

        if filename:    

            with open(filename, "rb") as attachment:  # Open PDF file in readable binary mode
                part = MIMEBase("application", "octet-stream")   # Add file as application/octet-stream
                attach_data = attachment.read()
                part.set_payload(attach_data)  # Email client can usually download this automatically as attachment

            encoders.encode_base64(part)  # Encode file in ASCII characters to send by email 

            

            part.add_header(
                "Content-Disposition",
                "attachment; filename={}".format(attach_name)
            )
            
            message.attach(part)   
        
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        #     server.login(sender_email, password)
        #     server.sendmail(
        #         sender_email, receiver_email, message.as_string()
        #         )

        resp = send_email_postmark(receiver_email, msg_subject, email_body, 
                file_path=None, attachment_content=attach_data, attachment_name=attach_name)

        print(resp)




def set_email_read_feedback(**kwargs):

    variables = encode_param(**kwargs)
    link = url_for("admin.report_email_receipt", 
            ref=variables, 
            _external=True)
    return link



def generate_pdf(_template, args, kwargs, email_body_template, pay_history=[]):

    env = Environment(loader=FileSystemLoader('applib/templates/'))

    template = env.get_template(_template)
    _template = template.render(posts=args, payments=pay_history, **kwargs)
    
    file_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    pdf_output = '{}_{}.pdf'.format(kwargs['type'], 
                                file_prefix)

    pdf_output = os.path.join("tmp_pdf", pdf_output)

    mode = get_config("mode")

    if mode == '1':
        file_path = 'tmp/content{}.html'.format(file_prefix)
        with open(file_path, 'w') as fl:
            fl.write(_template)

        bin_path = "./tmp/wkhtmltox/bin/wkhtmltopdf"
        sc.call([bin_path, file_path, pdf_output])

    else:
        pdfkit.from_string(_template, pdf_output)
    

    message_subject = kwargs['type']+" Generated for "+ kwargs['name'].upper()

    _link = set_email_read_feedback(email_receiver=kwargs['email'], 
                                    email_title=message_subject)

    template1 = env.get_template(email_body_template)
    _template1 = template1.render(items=args, payments=pay_history, status_link=_link, **kwargs)

    send_email(pdf_output, kwargs['email'], message_subject, _template1, kwargs['type'])


def comma_separation(amt):
    _len = len(str(amt))
    fmt = '{:' + str(_len) + ',.2f}' 
    return fmt.format(float(amt))




def set_pagination(obj, cur_page, page_size=10):
    
    pg = abs(cur_page)
    pager = paginate(obj, pg, page_size)
 
    start_no = pg - 1 
    if start_no < 1:
        start_no = pg

    counter = 0
    page_lists = []

    for x in range(start_no, pager.pages + 1 ):
        page_lists.append(x)
        counter += 1 
        if counter > 7:
            break

    return  pager, page_lists


def calc_discount(query_disc_type, query_disc_value, query_sub_total):
    
    discount = 0
    
    if query_disc_type == 'fixed':
        discount = query_disc_value

    elif query_disc_type == 'percent':
        discount = query_disc_value / 100 * query_sub_total

    return discount



def val_calculated_data(query_disc_type, query_disc_value, query_sub_total, query_obj):

    vat = 0
    vat_total = 0
    total = 0

    discount = calc_discount(query_disc_type, query_disc_value, query_sub_total)

    total = float(query_sub_total - discount)

    if query_obj == 1:
        vat = -( 7.5/100 * total)
        vat_total = total
    else:
        vat = 7.5/100 * total
        vat_total = total + vat
    
    return vat_total, vat, total, discount



def float2decimal(value):
    return Decimal(str(value))



def attach_functn(file_path):
    with open(file_path, 'rb') as f:
            data = f.read()
        
    encoded = base64.b64encode(data).decode()
    return encoded


def send_email_postmark(receiver_email, msg_subject, email_body, file_path=None, attachment_content=None, attachment_name="", attach_type="application/pdf"):


    cfg = get_config('mapappemail')

    params = {
            "From": cfg['sender'],
            "To": receiver_email,
            "Subject": msg_subject,
            "HtmlBody": email_body,
            "MessageStream": "outbound"
        }

    if file_path:
        attachment = attachment_content or attach_functn(file_path)
        params['Attachments'] = [
                {
                  "Name": attachment_name,
                  "Content": attachment,
                  "ContentType": attach_type
                }
            ]

    payload = json.dumps(params)

    
    headers = {"X-Postmark-Server-Token": cfg['key'],
                "Content-Type": "application/json", "Accept": "application/json"}


    r = rq.post(cfg["postmark"], data=payload, headers=headers)

    return r.text


def get_month_range(year, month):

    dt = datetime.datetime.now()
    rng = calendar.monthrange(year, month)

    start = dt.replace(year=year, month=month, day=1,hour=0, minute=0, second=1)
    end = dt.replace(year=year, month=month, day=rng[1],hour=23, minute=59, second=59)

    return start, end



