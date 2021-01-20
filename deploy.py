

import os 
import argparse 
import subprocess as s 


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


def set_args():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-w', "--worker", type=int, 
                        help='To set the number of workers involved',
                        default=1)

    parser.add_argument('-l', "--setlog", help="To set the log level", 
                        default='debug')

    parser.add_argument('-r', '--reload', 
                        action="store_true", 
                        help="this will set gunicorn to reload on any file changes",
                        default=False)

    parser.add_argument('-t', "--port",
    					help='pass this argument to drop all existing tables',
                        default=8000, type=int)

    parser.add_argument('-p', '--pyenv', default=None, help='set the python path')


    parser.add_argument('-f', '--logfile',
                        action="store_true", help='the gunicorn logger',
                        default=False
                        )
    parser.add_argument('-s', '--session', default=60, type=int, help='session timeout setting')
    parser.add_argument('-g', '--graceperiod', default=60, type=int, help='gracefull timeout period setting')



    return parser.parse_args()



# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


def init():

    options = set_args()

    exec_name = 'gunicorn'
    _opt = [exec_name, '-w %d'%options.worker]
    
    if options.pyenv:        
        exec_name = os.path.join(options.pyenv, 'bin/%s'%exec_name)
        _opt[0] = exec_name


    if options.reload:
        _opt.append('--reload')


    _opt.append('--log-level=%s'%options.setlog)
    
    _opt.append(f'--timeout={options.session}')
    _opt.append(f"--graceful-timeout={options.graceperiod}")
    _opt.append(f"--bind=:{options.port}")
    
    _opt.append("serve:create_app()")





    s.call(_opt)



# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


if __name__ == '__main__':
    # start the gunicorn (wsgi) server here
    init() 



