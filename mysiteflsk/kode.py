from flask import Flask, render_template, g, request, flash
import sqlite3
import os
from CDataBase import CDataBase


DATABASE = 'myflsksite.db'
DEBUG = True
SECRET_KEY = 'a21e6b7c27dcd76a843b31af6411608cabe783d9'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'myflsksite.db')))


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


@app.route("/")
@app.route("/catalog")
def catalog():
    db = get_db()
    dbase = CDataBase(db)
    return render_template('catalog.html', title="Каталог курсов", menu=dbase.get_menu(), courses=dbase.get_cours_anonce())


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/cours", methods=["POST", "GET"])
def cours():
    db = get_db()
    dbase = CDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['cours']) > 10:
            res = dbase.cours(request.form['name'], request.form['cours'], request.form['url'])
            if not res:
                flash('Ошибка добавления курса', category='error')
            else:
                flash('Курс добавлен успешно', category='success')
        else:
            flash('Ошибка добавления курса', category='error')
    return render_template('cours.html', title="Добавить курс", menu=dbase.get_menu())


@app.route("/info")
def info():
    db = get_db()
    dbase = CDataBase(db)
    return render_template('info.html', title="Информация", menu=dbase.get_menu())


if __name__ == '__main__':
    app.run(debug=True)