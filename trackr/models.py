from flask_login import UserMixin
from google.cloud import ndb


class User(UserMixin, ndb.Model):
    username = ndb.model.StringProperty(required=True, indexed=True)
    password = ndb.model.StringProperty(required=True)
    date_created = ndb.model.DateTimeProperty(required=True, auto_now_add=True)

    def get_id(self):
        return str(self.username)


class Category(ndb.Model):
    name = ndb.model.StringProperty(required=True)
    parent = ndb.model.KeyProperty(kind='Category')


class Transaction(ndb.Model):
    date = ndb.model.DateProperty(required=True)
    amount = ndb.model.FloatProperty(required=True)
    description = ndb.model.StringProperty()
    merchant = ndb.model.StringProperty()
    category = ndb.model.KeyProperty(kind='Category')
