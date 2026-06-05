from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def root():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))

@dashboard_bp.route("/dashboard")
@login_required
def index():
    if current_user.role == "admin":
        return render_template("dashboard/admin.html")
    return render_template("dashboard/employee.html")