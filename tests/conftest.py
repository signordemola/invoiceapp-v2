import pytest
from sqlalchemy import text
from applib.model import Base, Engine, sql_cursor
from serve import create_app

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SERVER_NAME': 'localhost',
        'APPLICATION_ROOT': '/',
        'PREFERRED_URL_SCHEME': 'http',
        'SQLALCHEMY_DATABASE_URI': 'postgresql+psycopg2://postgres:admin12345@localhost:5432/test_invoicedb',
    })
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    Base.metadata.create_all(Engine)

    with sql_cursor() as session:
        yield session
    with Engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS payment CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS item CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS email_queue CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS email_receipt_count CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS invoice CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS recurrent_bill CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS client CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS expense CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        conn.commit()