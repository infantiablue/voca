# from flask.globals import current_app
import requests
import os
import json
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, redirect, jsonify, flash, abort, current_app, url_for
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


@bp.route('/words/browse/page/<int:page>')
@bp.route('/words/browse')
@login_required
def browse(page=1):
    # Pagination
    words = current_user.words.order_by(
        'text').paginate(page, per_page=current_app.config['WORDS_PER_PAGE'])
    next_url = url_for('word.browse', page=words.next_num) \
        if words.has_next else None
    prev_url = url_for('word.browse', page=words.prev_num) \
        if words.has_prev else None
    total_words = current_user.words.count()
    base_num = int(total_words/3)
    remainder = total_words % 3
    # TODO: if 30 items?
    col1_n = col2_n = col3_n = base_num
    if remainder == 1:
        col1_n += 1
    if remainder == 2:
        col1_n += 1
        col2_n += 1
    col1 = []
    col2 = []
    col3 = []
    for idx, val in enumerate(words.items):
        if idx < col1_n:
            col1.append(val)
        if idx < col1_n + col2_n and idx >= col1_n:
            col2.append(val)
        if idx < col1_n + col2_n + col3_n and idx >= col1_n + col2_n:
            col3.append(val)
    cols = [col1, col2, col3]

    return render_template('word/browse.html', words=words, total_words=total_words, cols=cols, next_url=next_url,  prev_url=prev_url)


@bp.route('/sense/<word>')
@login_required
def sense(word):
    w = current_user.words.filter_by(text=word.lower()).first()
    if w:
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
        if note:
            note.text = form.note.data
        else:
            new_note = Note(text=form.note.data,
                            user_id=current_user.id, word_id=w.id)
            db.session.add(new_note)
        db.session.commit()
        flash("Updated note successfully.", category="success")
        return redirect(f'/edit/{word}')
    else:
        if(note):
            form.note.data = note.text
        if w:
            return render_template('word/edit.html', form=form, word=word)
    abort(404)


@bp.route('/word/remove', methods=['POST'])
@login_required
def remove():
    word = request.form['word']
    w = Word.query.filter_by(text=word).first()
    current_user.words.remove(w)
    db.session.commit()
    flash("The word has been removed successfully.", category="success")
    return jsonify({'message': "success"})


@bp.route('/api/lookup/<word>')
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

        url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + \
            language + '/' + word + '?fields=' + fields + '&strictMatch=' + strictMatch

        r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
        if (r.status_code == 200):
            res = r.json()
            w = []
            # Extracting crucial data from API result
            if 'results' in res:
                for r in res['results']:
                    res = []
                    for l in r['lexicalEntries']:
                        t = {}
                        t['lexical'] = l["lexicalCategory"]["text"].lower()
                        t['entry'] = []
                        if 'entries' not in l:
                            return {}, 404
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
                return {}, 404
        else:
            current_app.logger.error(
                f'API credential issue with HTTP CODE {r.status_code} ID {app_id} and KEY {app_key}')
            return {}, r.status_code
