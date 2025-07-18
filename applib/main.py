from flask import Flask
from flask_restful import Api


from flask_login import LoginManager

from applib.lib import helper  as h
 
# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Flask(__name__)

# app.config.update({
#                     "SQLALCHEMY_DATABASE_URI": h.set_db_uri(),
#                     'SQLALCHEMY_ECHO': True,
#                     'SQLALCHEMY_TRACK_MODIFICATIONS': False,
#                   })
#
# db = SQLAlchemy(app)

  
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login.login'

# declared here so that the db object would be set before introducing the model module

from applib import model as m 
import applib.sub_routes.login as adm
import applib.sub_routes.client as clt
import applib.sub_routes.expense as exp  
import applib.sub_routes.invoice as inv
import applib.sub_routes.item as itm
import applib.sub_routes.payment as pay
from applib.sub_routes import dashboard
from applib.sub_routes import billing


api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, 
    # use it in the query for the user
    return m.Users().get_user(user_id)


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


app.register_blueprint(adm.mod)
app.register_blueprint(clt.mod)
app.register_blueprint(exp.mod)
app.register_blueprint(inv.mod)
app.register_blueprint(itm.mod)
app.register_blueprint(pay.mod)
app.register_blueprint(dashboard.mod)
app.register_blueprint(billing.mod)


app.jinja_env.filters['date_format'] = h.date_format
app.jinja_env.filters['comma_sep'] = h.comma_separation




 