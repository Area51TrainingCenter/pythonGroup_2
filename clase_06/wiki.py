from flask import Flask, redirect, url_for, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wiki.db'
db = SQLAlchemy(app)


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), nullable=False, unique=True)
    body = db.Column(db.UnicodeText, nullable=False)


# /dsfsdf -> lectura
# /dsfsdf/edit -> edicion y creacion

@app.route('/', methods=['GET'])
@app.route('/<name>', methods=['GET'])
def lectura(name=None):
    if name is None:
        return redirect(url_for('lectura', name='defecto'))

    wiki = Entry.query.filter_by(name=name).first()

    return render_template('wiki.html', wiki=wiki, name=name)

@app.route('/<name>/edit', methods=['GET', 'POST'])
def edicion(name):
    wiki = Entry.query.filter_by(name=name).first()
    if wiki is None:
        wiki = Entry()
        wiki.name = name
    if request.method == 'GET':
        return render_template('wiki_edit.html', wiki=wiki, name=name)
    elif request.method == 'POST':
        wiki.body = request.form.get('body')
        db.session.add(wiki)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        else:
            return redirect(url_for('lectura', name=name))


if __name__ == '__main__':
    app.debug = True
    app.run()
