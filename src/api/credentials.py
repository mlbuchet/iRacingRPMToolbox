"""
File encapsulating the management of credentials.
"""

import os

def get_credentials():
    '''
    Obtains the credentials from environment variables.
    '''
    return {"user":os.getenv('IRAPI_USR'), "pwd":os.getenv('IRAPI_PWD')}
