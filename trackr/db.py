from flask import g
from google.cloud import ndb

def get_client():
    if 'client' not in g:
        g.client = ndb.Client()
    return g.client


def close_client():
    g.pop('client', None)


def init_db(app):
    app.teardown_appcontext(close_client)
    get_client()
