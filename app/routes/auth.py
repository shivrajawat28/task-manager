from flask import Blueprint, redirect, render_template, session, flash, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

# ================= REGISTER =================
@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("User already exists", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

# ================= LOGIN =================
@auth_bp.route("/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = username
            flash("Login successful!", "success")
            return redirect(url_for("tasks.view_tasks"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

# ================= LOGOUT =================
@auth_bp.route("/logout")
def logout():
    session.pop('user', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("auth.login"))
