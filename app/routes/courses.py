from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from app.extensions import db
from app.models.course import Course

courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/", methods=["GET"])
@login_required
def get_all_courses():
    if current_user.role != "admin":
        abort(403)

    courses = db.session.query(Course).all()
    return render_template("courses/index.html", courses=courses)

@courses_bp.route("/new", methods=["GET", "POST"])
@login_required
def courses():
    if current_user.role != "admin":
        abort(403)

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")
        thumbnail_url = request.form.get("thumbnail_url")
        
        if not title or not description or not category or not thumbnail_url:
            flash("All fields are required. ","danger")
            return redirect(url_for("courses.courses"))

        course = Course(title=title, description=description, category=category, thumbnail_url=thumbnail_url)
        db.session.add(course)
        db.session.commit()
        
        return redirect(url_for("courses.get_all_courses"))

    return render_template("courses/new.html")

@courses_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_course(id):
    course = db.session.get(Course, id)
    if course is None:
        abort(404)
    return render_template("courses/detail.html", course=course)


@courses_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_course(id):
    if current_user.role != "admin":
        abort(403)

    course = db.session.get(Course, id)
    if course is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")
        thumbnail_url = request.form.get("thumbnail_url")
        
        if not title or not description or not category or not thumbnail_url:
            flash("All fields are required. ","danger")
            return redirect(url_for("courses.edit_course", id=id))
        
        course.title = title
        course.description = description
        course.category = category
        course.thumbnail_url = thumbnail_url
        db.session.commit()

        return redirect(url_for("courses.get_all_courses"))
    return render_template("courses/edit.html", course=course)

@courses_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_course(id):
    if current_user.role != "admin":
        abort(403)

    course = db.session.get(Course, id)
    if course is None:
        abort(404)

    db.session.delete(course)
    db.session.commit()
    return redirect(url_for("courses.get_all_courses"))