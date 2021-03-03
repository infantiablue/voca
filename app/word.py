import requests
import json
from flask import Blueprint, render_template, request, redirect, jsonify, flash
from wtforms import Form, StringField, validators

bp = Blueprint('word', __name__)


class AddWordForm(Form):
    word = StringField('Word', [
        validators.DataRequired(),
        validators.Length(min=3, max=30),
    ])


@bp.route('/words/list')
def dashboard():
    return 'List'


@bp.route('/word/add', methods=['GET', 'POST'])
def add():
    form = AddWordForm(request.form)
    if request.method == 'POST' and form.validate():
        # TODO
        flash("A new word has been added.")
        # Redirect user to home page
        return redirect('/')
    return render_template('word/add.html', form=form)


@bp.route('/word/edit')
def edit():
    return 'Edit'


@bp.route('/word/delete')
def account():
    return 'Delete '


@bp.route('/api/lookup/<word>')
def lookup(word):
    app_id = 'fd0f1799'
    app_key = 'b07f95f839de63b54d400c2f023658d3'
    language = 'en-gb'
    fields = 'definitions%2Cexamples'  # TODO: escape URL
    strictMatch = 'false'

    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + \
        '/' + word.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch

    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
    res = r.json()
    word = []
    print(res)
    if 'results' in res:
        for r in res['results']:
            res = []
            for l in r['lexicalEntries']:
                t = {}
                t['lexical'] = l["lexicalCategory"]["text"].lower()
                t['entry'] = []
                for e in l['entries']:
                    for s in e['senses']:
                        m = []
                        if 'examples' in s:
                            for ex in s['examples']:
                                m.append(ex)
                        for d in s['definitions']:
                            t['entry'].append(
                                {'definition': d, 'examples': m})

                res.append(t)
            word.append({'result': res})
        return(jsonify(word))
    else:
        return 404, {}
