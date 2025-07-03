
import os
import argparse
import logging
from werkzeug.debug import DebuggedApplication


from applib.main import app
from applib.lib.helper import get_config, set_db_uri
from applib.model import create_tables, drop_tables


def create_app(): 
    
    cfg = get_config('server')
    app.config.update(
        **cfg
    )
 
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

def main():

    cmd = get_commands()

    if cmd.create_tl:
        create_tables()
        print("all missing tables have been recreated from scratch")
        return

    if cmd.drop_tl:
        drop_tables()
        print("all tables dropped from the database")
        return

    # main app starts here
    
    create_app().run()



def get_commands():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', "--create_tl", action='store_true',
                        help='pass this argument to create missing tables',
                        default=False)

    parser.add_argument('-d', "--drop_tl", action='store_true',
                        help='pass this argument to drop all existing tables',
                        default=False)

    


    return parser.parse_args()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

if __name__ == '__main__':
    main()
