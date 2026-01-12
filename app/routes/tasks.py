#here we make tasks routes
#importing all the required libraries

from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from sqlalchemy.engine import url
from app import db
from app.models import Task

task_bp = Blueprint('tasks', __name__)  #task_bp ka ek bluepring object bnaya

#view task route
@task_bp.route("/")
def view_tasks():
    #checking if user in session or not
    if 'user' not in session:
        return redirect(url_for("auth.login"))

    #showing their tasks
    tasks = Task.query.all()


    # ===== Progress calculation =====
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status="Done").count()

    if total_tasks == 0:
        progress = 0
    else:
        progress = int((completed_tasks / total_tasks) * 100)
    # ================================

    return render_template("task.html", tasks=tasks, progress=progress)


#add task route
@task_bp.route("/add", methods = ['POST'])
def add_task():
    if 'user' not in session:
        return redirect(url_for("auth.login"))

    #adding task
    title = request.form.get("title")
    if title:
        new_task = Task(title = title, status = "Pending")
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully", "success")
    
    return redirect(url_for("tasks.view_tasks"))


#toggle route
@task_bp.route("/toggle/<int:task_id>", methods=['POST'])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == "Working":
            task.status = 'Done'
        else:
            task.status = 'Pending'
        db.session.commit()
    
    return redirect(url_for("tasks.view_tasks"))


#all task clear route
@task_bp.route("/clear", methods = ['POST'])
def clear_tasks():
    Task.query.delete()
    db.session.commit()
    flash("All task cleard", "info")
    return redirect(url_for("tasks.view_tasks"))



#delete any existing task
@task_bp.route("/delete<int:task_id>", methods=['POST'])
def delete_task(task_id):
    if 'user' not in session:
        return redirect(url_for("auth.login"))

    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully", "danger")

    return redirect(url_for("tasks.view_tasks"))


