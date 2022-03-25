import os

def get_credentials():
    return {"user":os.getenv('IRAPI_USR'), "pwd":os.getenv('IRAPI_PWD')}
