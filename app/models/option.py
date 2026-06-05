from app.extensions import db

class Option(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    question = db.relationship("Question", back_populates="options")
    text = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean , nullable=False)

    quiz_answers = db.relationship("QuizAnswer", back_populates="option")

    def __repr__(self):
        return f"<Option {self.text}>"
