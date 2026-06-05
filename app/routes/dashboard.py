from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def index():
    if current_user.role == "admin":
        return render_template("dashboard/admin.html")
    return render_template("dashboard/employee.html")