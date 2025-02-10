# Program to implement to-do-list:
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase
import os

flag = 0
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)

# Table:
class Todo(db.Model):
    id:Mapped[int] = mapped_column(Integer,autoincrement=True,primary_key=True)
    task:Mapped[String] = mapped_column(String)
    accomplish:Mapped[int] = mapped_column(Integer)

app = Flask(__name__)
app.config["SECRET_KEY"]  = "Ilikeyoumarfii"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    global flag
    result = db.session.execute(db.select(Todo).where(Todo.accomplish == flag)).scalars()
    return render_template("home.html",data = result)

# Insert data:
@app.route("/add_task",methods = ["POST"])
def add_task():
    if request.method == "POST":
        task = Todo(
            task = request.form["task"],
            accomplish = 0,
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))

# Changing status:
@app.route("/update_status/<int:tid>")
def change_status(tid):
    fetch = db.session.execute(db.select(Todo).where(Todo.id == tid)).scalar()
    fetch.accomplish = 1
    db.session.commit()
    return redirect(url_for('home'))

# Deleting Task:
@app.route("/delete_task/<int:tid>")
def delete_task(tid):
    fetch = db.session.execute(db.select(Todo).where(Todo.id == tid)).scalar()
    db.session.delete(fetch)
    db.session.commit()
    return redirect(url_for('home'))

# Filtering out tasks:
@app.route("/filter_task",methods = ["POST"])
def filter_out():
    global flag
    if request.method == "POST":
        flag = request.form["tasks"]
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

