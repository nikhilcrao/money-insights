from google.cloud import ndb


class Category(ndb.Model):
    name = ndb.model.StringProperty(required=True)
    parent = ndb.model.KeyProperty(kind='Category')


class Transaction(ndb.Model):
    date = ndb.model.DateProperty(required=True)
    amount = ndb.model.FloatProperty(required=True)
    description = ndb.model.StringProperty()
    merchant = ndb.model.StringProperty()
    category = ndb.model.KeyProperty(kind='Category')
