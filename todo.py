from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.secret_key = "EPj00jpfj8Gx1SjnyLxwBBSQfnQ9DJYe0Ym"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Lenovo/Documents/python_proje/todo_app/todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    list = Todo.query.order_by(desc("id")).all()
    return render_template("index.html", list = list)

@app.route("/complete/<string:id>")
def complete(id):
    todo = Todo.query.filter_by(id = id).first() 
    todo.complete = not todo.complete
    db.session.commit()
    flash("Row marked as complete", "success")
    return redirect(url_for("index"))

@app.route("/remove/<string:id>")
def remove(id):
    todo = Todo.query.filter_by(id = id).delete()
    db.session.commit()
    flash("Row removed successfully", "success")
    return redirect(url_for("index"))

@app.route("/add", methods = ["POST"])
def add():
    title = request.form.get("title")
    newTodo = Todo(title = title, complete = False)
    db.session.add(newTodo)
    db.session.commit()

    flash("Row added", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
