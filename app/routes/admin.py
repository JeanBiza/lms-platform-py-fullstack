from flask import Blueprint, redirect, render_template, url_for, abort, request, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.extensions import db

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users")
@login_required
def get_users():
    if current_user.role != "admin":
        abort(403)

    employees = User.query.filter_by().all()
    return render_template("admin/admin.html", employees=employees)


@admin_bp.route("/users/new", methods=["POST", "GET"])
@login_required
def new_user():
    if current_user.role != "admin":
        abort(403)
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")
        department = request.form.get("department")
        active = request.form.get("active")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("This email is already associated with an account. ", "danger")
            return redirect(url_for("admin.new_user"))
        
        if password != confirm_password:
            flash("passwords don't match. ", "danger")
            return redirect(url_for("admin.new_user"))  

        user = User(name=name, email=email, role=role, department=department, active=active)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("admin.get_users")) 
    
    return render_template("admin/new_user.html")
    

@admin_bp.route("/users/<int:id>/delete", methods=["POST"])
@login_required
def delete_user(id):
    if current_user.role != "admin":
        abort(403)

    user = db.session.get(User, id)

    if not user:
        flash("User doesn't exist.  ", "danger")
        return redirect(url_for("admin.get_users")) 

    if user.role == "admin":
        flash("Cannot delete a Admin user.  ", "danger")
        return redirect(url_for("admin.get_users")) 
    
    if user.id == current_user.id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("admin.get_users"))
    
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin.get_users"))

@admin_bp.route("/users/<int:id>/toggle-role", methods=["POST"])
@login_required
def toggle_role(id):
    if current_user.role != "admin":
        abort(403)

    user = db.session.get(User, id)

    if not user:
        flash("User doesn't exist.  ", "danger")
        return redirect(url_for("admin.get_users")) 

    user.role = "employee" if user.role == "admin" else "admin"
    db.session.commit()

    return redirect(url_for("admin.get_users"))

