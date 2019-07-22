def _init():
    global DB_USER, DB_PASS, DB_NAME, DB_HOST

    import os
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_HOST = os.environ['DB_HOST']

_init()
