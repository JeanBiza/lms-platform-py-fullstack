from app.extensions import db
import datetime

class QuizAttempt(db.Model):
    __tablename__ = "quizzes_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="quiz_attempts")
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    quiz = db.relationship("Quiz", back_populates="quiz_attempts")

    score = db.Column(db.Integer , nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    attempted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    quiz_answers = db.relationship("QuizAnswer", back_populates="attempt", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Quiz Attempt {self.id}>"