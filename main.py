import datetime
import google.oauth2.id_token

from flask import Flask, render_template, request, redirect
from google.auth.transport import requests
from google.cloud import datastore

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'test',
})

datastore_client = datastore.Client()

firebase_request_adapter = requests.Request()

def store_time(email, dt):
    entity = datastore.Entity(key=datastore_client.key('User', email, 'visit'))
    entity.update({
        'timestamp': dt,
    })
    datastore_client.put(entity)


def fetch_times(email, limit):
    ancestor = datastore_client.key('User', email)
    query = datastore_client.query(kind='visit', ancestor=ancestor)
    query.order = ['-timestamp']
    times = query.fetch(limit=limit)
    return times


def store_category(email, name):
    entity = datastore.Entity(key=datastore_client.key('User', email, 'category'))
    entity.update({
        'name': name,
    })
    datastore_client.put(entity)


def fetch_categories(email, limit=None):
    ancestor = datastore_client.Key('User', email)
    query = datastore_client.query(kind='category', ancestor=ancestor)
    categories = query.fetch(limit=limit)
    return categories


@app.route('/')
def root():
    id_token = request.cookies.get('token')
    error_message = None
    claims = None
    times = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            store_time(claims['email'], datetime.datetime.now())
            times = fetch_times(claims['email'], 10)
        except ValueError as err:
            error_message = str(err)

    return render_template('index.html', user_data=claims, error_message=error_message, times=times)


@app.route('/category/', methods=['GET'])
def category_home():
    id_token = request.cookies.get('token')
    error_message = None
    claims = None
    categories = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            categories = fetch_categories(claims['email'])
        except ValueError as err:
            error_message = str(err)

    return render_template('category_index.html', user_data=claims, error_message=error_message, categories=categories)



class AddCategoryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


@app.route('/category/add', methods=['GET', 'POST'])
def add_category():
    form = AddCategoryForm()
    if form.validate_on_submit():
        id_token = request.cookies.get('token')
        error_message = None
        claims = None
        categories = None

        if id_token:
            try:
                claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
                store_category(claims['email'], form.name)
                return redirect('/category/')
            except ValueError as err:
                error_message = str(err)


    return render_template('category_add.html', form=form)


@app.route('/category/edit/<category_slug>')
def edit_category(category_slug):
    pass


@app.route('/category/remove/<category_slug>')
def remove_category(category_slug):
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
