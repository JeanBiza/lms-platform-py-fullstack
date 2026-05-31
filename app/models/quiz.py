from app.extensions import db

class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    course = db.relationship("Course", back_populates="quiz")
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    passing_score = db.Column(db.Integer, nullable=False)

    questions = db.relationship("Question", back_populates="quiz")
    quiz_attempts = db.relationship("QuizAttempt", back_populates="quiz")

    def __repr__(self):
        return f"<Quiz {self.id}>"
