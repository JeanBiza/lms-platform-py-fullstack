import datetime

from flask import Blueprint, abort, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.lesson_progress import LessonProgress
from app.models.lesson import Lesson
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
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    
    progress_data = []
    for enrollment in enrollments:
        course = db.session.get(Course, enrollment.course_id)
        total_lessons = len(course.lessons)
        completed_lessons = LessonProgress.query.filter_by(
            user_id=current_user.id
        ).join(Lesson).filter(Lesson.course_id == course.id).count()
        
        percent = round(completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        progress_data.append({
            "course": course,
            "enrollment": enrollment,
            "completed": completed_lessons,
            "total": total_lessons,
            "percent": percent
        })
    
    return render_template("dashboard/my_progress.html", progress_data=progress_data)

@employee_bp.route("/lessons/<int:lesson_id>/complete", methods=["POST"])
@login_required
def complete_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)
    if not lesson:
        abort(404)

    lesson_progress = LessonProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
    if not lesson_progress:
        lesson_progress = LessonProgress(user_id=current_user.id, lesson_id=lesson_id)
        db.session.add(lesson_progress)

    db.session.commit()

    course = lesson.course
    total = len(course.lessons)
    completed = LessonProgress.query.filter_by(
        user_id=current_user.id
    ).join(Lesson).filter(Lesson.course_id == course.id).count()

    if total > 0 and completed >= total:
        enrollment = Enrollment.query.filter_by(
            user_id=current_user.id, course_id=course.id
        ).first()
        if enrollment:
            enrollment.status = "completed"
            enrollment.completed_at = datetime.datetime.utcnow()
            db.session.commit()

    return redirect(url_for("employee.my_progress"))

@employee_bp.route("/lessons/<int:lesson_id>", methods=["GET"])
@login_required
def view_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)
    if not lesson:
        abort(404)

    already_completed = LessonProgress.query.filter_by(
        user_id=current_user.id, lesson_id=lesson_id
    ).first() is not None

    return render_template("dashboard/lesson.html", lesson=lesson, already_completed=already_completed)