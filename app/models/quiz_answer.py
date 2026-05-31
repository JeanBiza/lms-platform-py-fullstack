from app.extensions import db

class QuizAnswer(db.Model):
    __tablename__ = "quizzes_answers"

    id = db.Column(db.Integer, primary_key=True)
    attempt = db.relationship("QuizAttempt", back_populates="quiz_answers")
    attempt_id = db.Column(db.Integer, db.ForeignKey("quizzes_attempts.id") ,nullable=False)
    question = db.relationship("Question", back_populates="quiz_answers")
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id") ,nullable=False)
    option = db.relationship("Option", back_populates="quiz_answers")
    option_id = db.Column(db.Integer, db.ForeignKey("options.id") ,nullable=False)
    

    def __repr__(self):
        return f"<Quiz Answer {self.id}>"