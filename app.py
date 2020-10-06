from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from instance.database import SQLALCHEMY_DATABASE_URI as DATABASE_URI
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SEACRET_KEY = os.urandom(24)
db = SQLAlchemy(app)


# モデル
class Task(db.Model):

  __tablename__ = "tasks"
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.String)
  task_type = db.Column(db.String)
  priority = db.Column(db.Integer)
  title = db.Column(db.String)
  text = db.Column(db.String)


# index.html
@app.route('/', methods=['POST','GET'])
def index():
  if request.method == 'POST':
    task = Task()
    task.date = str(datetime.today().year) + "/" + str(datetime.today().month) + "/" + str(datetime.today().day) + " " + str(datetime.today().hour) + "/" + str(datetime.today().minute)
    task.task_type = request.form.get('task_type')
    task.priority = request.form.get('priority')
    task.title = request.form.get('title')
    task.text = request.form.get('text')

    try:
      db.session.add(task)
      db.session.commit()
      return redirect('/')
    except:
      return "add failed"

  else:
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


# /delete
@app.route('/delete/<int:id>')
def delete(id):
  task = Task.query.get(id)

  try:
    db.session.delete(task)
    db.session.commit()
    db.session.close()
    return redirect('/')
  except:
    return 'There was an problem deleting that task'


# /edit
@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
  task = Task.query.get(id)
  return render_template('edit.html', task=task)

# /update
@app.route('/update/<int:id>', methods=["GET","POST"])
def update(id):
    task = Task.query.get(id)

    if request.method == 'POST':
      task.date = str(datetime.today().year) + "/" + str(datetime.today().month) + "/" + str(datetime.today().day) + " " + str(datetime.today().hour) + "/" + str(datetime.today().minute) 
      task.task_type = request.form.get('task_type')
      task.priority = request.form.get('priority')
      task.title = request.form.get('title')
      task.text = request.form.get('text')

      try:
        db.session.add(task)
        db.session.commit()
        return redirect('/')
      except:
        return "edit failed"

    else:
      return render_template('edit.html',tasks=tasks)


if __name__ == "__main__":
  app.run()