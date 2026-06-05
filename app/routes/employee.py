from flask import Blueprint, abort, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.extensions import db

employee_bp = Blueprint("employee", __name__)

@employee_bp.route("/catalog", methods=["GET"])
@login_required
def catalog():
    courses = Course.query.filter_by(is_active=True).all()
    enrolled_course_ids = [enrollment.course_id for enrollment in current_user.enrollments]
    return render_template("dashboard/catalog.html", courses=courses, user=current_user, enrolled_course_ids=enrolled_course_ids)


@employee_bp.route("/enroll/<int:course_id>", methods=["POST"])
@login_required
def enroll(course_id):
    membership = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if membership:
        abort(400, description="Already enrolled in this course.")

    new_enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    db.session.add(new_enrollment)
    db.session.commit()

    return redirect(url_for("employee.my_progress"))


@employee_bp.route("/my-progress")
@login_required
def my_progress():
    return "Here will be your progress page! Content coming soon."
