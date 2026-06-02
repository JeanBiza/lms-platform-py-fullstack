from flask import Flask
from app.extensions import db, migrate, login_manager
from config import Config
from app.models.user import User
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.option import Option
from app.models.enrollment import Enrollment
from app.models.lesson_progress import LessonProgress
from app.models.quiz_attempt import QuizAttempt
from app.models.quiz_answer import QuizAnswer
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.courses import courses_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(courses_bp, url_prefix="/courses")
    return app