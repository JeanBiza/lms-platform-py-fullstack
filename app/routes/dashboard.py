from flask import Blueprint, redirect, render_template, url_for, abort
from flask_login import login_required, current_user
from app.models.enrollment import Enrollment
from app.models.lesson_progress import LessonProgress
from app.models.lesson import Lesson
from app.models.user import User
from app.models.course import Course

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def root():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("dashboard.index_admin"))
        else:
            return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))


@dashboard_bp.route("/dashboard")
@login_required
def index():
    if current_user.role == "admin":
        return redirect(url_for("dashboard.index_admin")) 
    
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

@dashboard_bp.route("/dashboard/admin")
@login_required
def index_admin():
    if current_user.role != "admin":
        abort(403)
    
    total_users = User.query.filter_by(role="employee").count()
    total_courses = Course.query.filter_by(is_active=True).count()
    total_inscriptions = Enrollment.query.count()

    employees = User.query.filter_by(role="employee").all()

    employee_data = []
    for employee in employees:
        enrollments = Enrollment.query.filter_by(user_id=employee.id).all()
        completed = sum(1 for e in enrollments if e.status == "completed")
        employee_data.append({
            "user": employee,
            "enrolled": len(enrollments),
            "completed": completed
        })

    recent_enrollments = Enrollment.query.order_by(
        Enrollment.enrolled_at.desc()
    ).limit(5).all()

    return render_template("dashboard/admin.html",
                           total_users=total_users,
                           total_courses=total_courses,
                           total_inscriptions=total_inscriptions,
                           employee_data=employee_data,
                           recent_enrollments=recent_enrollments)