# from flask.globals import current_app
import requests
import os
import json
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, redirect, jsonify, flash, abort
from wtforms import Form, StringField, TextAreaField, validators
from .models import db, Word, Note

bp = Blueprint('word', __name__)


class AddWordForm(Form):
    word = StringField('Word', [
        validators.DataRequired(),
        validators.Length(min=3, max=30),
    ])


class EditWordForm(Form):
    note = TextAreaField('Note', [])


@bp.route('/words/list')
@login_required
def dashboard():
    return 'List'


@bp.route('/sense/<word>')
@login_required
def sense(word):
    w = current_user.words.filter_by(text=word.lower()).first()
    if w:
        # w = current_user.words.filter_by(text=word).first()
        note = Note.query.filter_by(
            user_id=current_user.id, word_id=current_user.words.filter_by(text=word).first().id).first()
        note_text = ''
        if note:
            note_text = note.text.replace(w.text, f'<u>{w.text}</u>')
        else:
            note_text = None
        try:
            with open(f'cache/{w.text}.json') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            flash("An error has been occured.", category="error")
        return render_template('word/sense.html', data=data, word=word, note=note_text)
    else:
        abort(404)


@ bp.route('/word/add', methods=['GET', 'POST'])
@ login_required
def add():
    form = AddWordForm(request.form)
    if request.method == 'POST' and form.validate():
        input_word = form.word.data.lower()
        word = Word.query.filter_by(text=input_word).first()
        if not word:
            new_word = Word(text=input_word)
            current_user.words.append(new_word)
            db.session.add(new_word)
        else:
            if not current_user.words.filter_by(text=input_word).first():
                current_user.words.append(word)
            else:
                flash("This word is duplicated.", category="error")
                return redirect(f'/sense/{input_word}')
        # Add new word to the database
        db.session.commit()

        flash("A new word has been added.", category="success")

        # Redirect user to new word page
        return redirect(f'/sense/{input_word}')
    return render_template('word/add.html', form=form)


@ bp.route('/edit/<word>', methods=['GET', 'POST'])
@ login_required
def edit(word):
    form = EditWordForm(request.form)

    if (word):
        w = current_user.words.filter_by(text=word).first()
        note = Note.query.filter_by(
            user_id=current_user.id, word_id=w.id).first()
    if request.method == 'POST' and form.validate():
        print('requesting')
        if note:
            note.text = form.note.data
        else:
            new_note = Note(text=form.note.data,
                            user_id=current_user.id, word_id=w.id)
            db.session.add(new_note)
        db.session.commit()
        return redirect(f'/edit/{word}')
    else:
        if(note):
            form.note.data = note.text
        if w:
            return render_template('word/edit.html', form=form, word=word)
    abort(404)


@ bp.route('/word/remove', methods=['POST'])
@ login_required
def remove():
    word = request.form['word']
    w = Word.query.filter_by(text=word).first()
    current_user.words.remove(w)
    db.session.commit()
    flash("The word has been removed successfully", category="success")
    return jsonify({'message': "success"})


@ bp.route('/api/lookup/<word>')
@ login_required
def lookup(word):
    word = word.lower()
    try:
        with open(f'cache/{word}.json') as json_file:
            data = json.load(json_file)
            return(jsonify(data))
    except FileNotFoundError:
        app_id = os.environ.get('OXFORD_APP_ID')
        app_key = os.environ.get('OXFORD_APP_KEY')
        language = 'en-gb'
        fields = 'definitions%2Cexamples'  # TODO: escape URL
        strictMatch = 'false'

        url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + \
            '/' + word + '?fields=' + fields + '&strictMatch=' + strictMatch

        r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
        res = r.json()
        w = []
        print(res)
        # Extracting crucial data from API result
        if 'results' in res:
            for r in res['results']:
                res = []
                for l in r['lexicalEntries']:
                    t = {}
                    t['lexical'] = l["lexicalCategory"]["text"].lower()
                    t['entry'] = []
                    if 'entries' not in l:
                        return {}
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
                w.append({'sense': res})
            with open(f'cache/{word}.json', 'w') as outfile:
                json.dump(w, outfile)
            return(jsonify(w))
        else:
            return {}
