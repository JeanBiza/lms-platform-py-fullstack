from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.models.enrollment import Enrollment
from app.models.lesson_progress import LessonProgress
from app.models.lesson import Lesson

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
    
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    
    progress_data = []
    for enrollment in enrollments:
        course = enrollment.course
        total = len(course.lessons)
        completed = LessonProgress.query.filter_by(
            user_id=current_user.id
        ).join(Lesson).filter(Lesson.course_id == course.id).count()
        percent = round(completed / total * 100) if total > 0 else 0
        progress_data.append({
            "course": course,
            "enrollment": enrollment,
            "percent": percent,
            "completed": completed,
            "total": total
        })

    total_enrolled = len(enrollments)
    total_completed = sum(1 for e in enrollments if e.status == "completed")
    total_in_progress = total_enrolled - total_completed

    return render_template("dashboard/employee.html",
        progress_data=progress_data,
        total_enrolled=total_enrolled,
        total_completed=total_completed,
        total_in_progress=total_in_progress
    )