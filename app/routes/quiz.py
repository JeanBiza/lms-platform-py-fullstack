from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from app.extensions import db
from app.models.quiz import Quiz
from app.models.course import Course
from app.models.question import Question
from app.models.option import Option
from app.models.quiz_answer import QuizAnswer
from app.models.quiz_attempt import QuizAttempt

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

@quiz_bp.route("/<int:course_id>/quiz/take", methods=["GET", "POST"])
@login_required
def take_quiz(course_id):
    course = db.session.get(Course, course_id)
    if course is None:
        abort(404)

    quiz = Quiz.query.filter_by(course_id=course_id).first()
    if quiz is None:
        abort(404)

    if request.method == "POST":

        quiz_attempt = QuizAttempt(user_id=current_user.id, quiz_id=quiz.id, score=0, passed=False)
        db.session.add(quiz_attempt)
        db.session.flush()

        correct = 0
        for question in quiz.questions:
            option_id = request.form.get(f"question_{question.id}")
            quiz_answer = QuizAnswer(attempt_id=quiz_attempt.id, question_id=question.id, option_id=option_id)
            db.session.add(quiz_answer)
            if option_id:
                option = db.session.get(Option, int(option_id))
                if option and option.is_correct:
                    correct += 1

        score = round(correct / len(quiz.questions) * 100)
        passed = score >= quiz.passing_score

        quiz_attempt.score = score
        quiz_attempt.passed = passed
        db.session.commit()


        return redirect(url_for("quiz.results", course_id=course_id, user_id=current_user.id))

    return render_template("quiz/quiz.html", course=course, quiz=quiz)


@quiz_bp.route("/<int:course_id>/quiz/results", methods=["GET"])
@login_required
def results(course_id):
    quiz = Quiz.query.filter_by(course_id=course_id).first()
    if quiz is None:
        abort(404)

    attempt = QuizAttempt.query.filter_by(
        user_id=current_user.id, quiz_id=quiz.id
    ).order_by(QuizAttempt.attempted_at.desc()).first()

    if attempt is None:
        abort(404)

    return render_template("quiz/results.html", quiz=quiz, attempt=attempt)