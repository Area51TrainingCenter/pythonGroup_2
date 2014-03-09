from flask import Flask, request, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class TODO(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), nullable=False, unique=True)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), nullable=False)
    done = db.Column(db.Boolean, default=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todos.id'))
    todo = db.relationship('TODO', backref=db.backref('items'))


@app.route('/todo/', methods=['GET', 'POST'])
@app.route('/todo/<name>', methods=['GET', 'POST'])
def plantilla(name=None):
    if name is None:
        return redirect(url_for('plantilla', name='defecto'))

    todo = TODO.query.filter_by(name=name).first()

    if todo is None:
        todo = TODO()
        todo.name = name
        items = []
    else:
        items = todo.items  # Item.query.filter_by(todo_id=todo.id).all()

    if request.method == 'POST':
        marked_items = request.form.getlist('items')
        for item in todo.items:
             item.done = (str(item.id) in marked_items)
             db.session.add(item)

        if len(request.form.get('new_item')) > 0:
            i = Item()
            i.name = request.form.get('new_item')
            todo.items.append(i)
            db.session.add(todo)
            db.session.add(i)

        try:
            db.session.commit()
        except:
            db.session.rollback()
        else:
            items = todo.items
        
    return render_template('index.html', name=todo.name, lista=items)


if __name__ == '__main__':
    app.debug = True
    app.run()
