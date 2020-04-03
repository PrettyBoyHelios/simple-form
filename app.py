from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from os import path

home = str(Path.home())
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + path.join(home, ".simple-form", "registry.db")
db = SQLAlchemy(app)


print("db file: ", app.config['SQLALCHEMY_DATABASE_URI'])


class Registry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(10))
    school = db.Column(db.String(200))


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == 'POST':
        student = Registry(name=request.form.get("name"), email=request.form.get("email"), phone=request.form.get("phone"), school=request.form.get("school"))
        print(student.__dict__)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('student_list'))


@app.route('/list', methods=['GET'])
def student_list():
    if request.method == "GET":
        students = Registry.query.all()
        return render_template("list.html", list=students)


if __name__ == '__main__':
    app.run(debug=True)
