from app.extensions import db
import datetime

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz = db.relationship("Quiz", back_populates="questions")
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id") ,nullable=False)
    text = db.Column(db.Text , nullable=False)
    order = db.Column(db.Integer, nullable=False)
    
    options = db.relationship("Option", back_populates="question", cascade="all, delete-orphan")
    quiz_answers = db.relationship("QuizAnswer", back_populates="question", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Question {self.text}>"
