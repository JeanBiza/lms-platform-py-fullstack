from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from app.extensions import db
from app.models.quiz import Quiz
from app.models.course import Course
from app.models.question import Question
from app.models.option import Option

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/<int:course_id>/quiz/new", methods=["GET", "POST"])
@login_required
def new_quiz(course_id):
    if current_user.role != "admin":
        abort(403)

    course = db.session.get(Course, course_id)
    if course is None:
        abort(404)

    if course.quiz:
        flash("This course already has a quiz.", "warning")
        return redirect(url_for("courses.get_course", id=course_id))

    if request.method == "POST":
        passing_score = request.form.get("passing_score", 70)

        quiz = Quiz(course_id=course.id, passing_score=int(passing_score))
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for("quiz.new_question", course_id=course_id, quiz_id=quiz.id))

    return render_template("quiz/new_quiz.html", course=course)

@quiz_bp.route("/<int:course_id>/quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def new_question(course_id, quiz_id):
    if current_user.role != "admin":
        abort(403)

    course = db.session.get(Course, course_id)
    if course is None:
        abort(404)

    quiz = db.session.get(Quiz, quiz_id)
    if quiz is None:
        abort(404)

    if request.method == "POST":
        question_text = request.form.get("text")
        order = request.form.get("order")

        question = Question(quiz_id=quiz_id, text=question_text, order=order)
        db.session.add(question)
        db.session.commit()

        correct_option_text = request.form.get("correct_option")
        option_text_1 = request.form.get("option_1")
        option_text_2 = request.form.get("option_2")
        option_text_3 = request.form.get("option_3")
        
        correct_option = Option(question_id=question.id, text=correct_option_text, is_correct=True)
        option1 = Option(question_id=question.id, text=option_text_1, is_correct=False)
        option2 = Option(question_id=question.id, text=option_text_2, is_correct=False)
        option3 = Option(question_id=question.id, text=option_text_3, is_correct=False)

        db.session.add_all([correct_option, option1, option2, option3])
        db.session.commit()

        return redirect(url_for("quiz.new_question", course_id=course_id, quiz_id=quiz.id))

    return render_template("quiz/new_question.html", course=course, quiz=quiz)

