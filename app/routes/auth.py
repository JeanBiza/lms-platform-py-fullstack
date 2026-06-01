from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect("/")

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        department = request.form.get("department")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("This email is already associated with an account. ", "danger")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("passwords don't match. ", "danger")
            return redirect(url_for("auth.register"))  
        

        user = User(name=name, email=email, department=department)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")