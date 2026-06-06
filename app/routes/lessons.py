from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from app.extensions import db
from app.models.lesson import Lesson
from app.models.course import Course

lessons_bp = Blueprint("lessons", __name__)

@lessons_bp.route("/<int:course_id>/lessons/new", methods=["GET", "POST"])
@login_required
def new_lesson(course_id):
    if current_user.role != "admin":
        abort(403)

    course = db.session.get(Course, course_id)
    if course is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title")
        order = request.form.get("order")
        type = request.form.get("type")
        content = request.form.get("content")
        
        if not title or not order or not type or not content:
            flash("All fields are required. ","danger")
            return redirect(url_for("lessons.new_lesson", course_id=course_id))
        
        existing = Lesson.query.filter_by(
            course_id=course_id, order=order
        ).first()
        if existing and existing.id != id: 
            flash("That order number is already taken.", "danger")
            return redirect(url_for("lessons.new_lesson", course_id=course_id))

        lesson = Lesson(course_id=course.id, title=title, order=order, type=type, content=content)
        db.session.add(lesson)
        db.session.commit()
        
        return redirect(url_for("courses.get_course", id=course_id))

    return render_template("lessons/new.html", course=course)


@lessons_bp.route("/<int:course_id>/lessons/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_lesson(id, course_id):
    if current_user.role != "admin":
        abort(403)

    course = db.session.get(Course, course_id)
    if course is None:
        abort(404)
    
    lesson = db.session.get(Lesson, id)
    if lesson is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title")
        order = request.form.get("order")
        type = request.form.get("type")
        content = request.form.get("content")
        
        if not title or not order or not type or not content:
            flash("All fields are required. ","danger")
            return redirect(url_for("lessons.edit_lesson", course_id=course_id, id=id))
        
        lesson.title = title
        lesson.order = order
        lesson.type = type
        lesson.content = content
        db.session.commit()

        return redirect(url_for("courses.get_course", id=course_id))
    return render_template("lessons/edit.html", lesson=lesson, course=course)

@lessons_bp.route("/<int:course_id>/lessons/<int:id>/delete", methods=["POST"])
@login_required
def delete_lesson(course_id, id):
    if current_user.role != "admin":
        abort(403)

    lesson = db.session.get(Lesson, id)
    if lesson is None:
        abort(404)

    db.session.delete(lesson)
    db.session.commit()
    return redirect(url_for("courses.get_course", id=course_id))