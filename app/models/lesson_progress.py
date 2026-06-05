from app.extensions import db
import datetime

class LessonProgress(db.Model):
    __tablename__ = "lesson_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="lesson_progress")
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    lesson = db.relationship("Lesson", back_populates="lesson_progress")
    completed_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Lesson Progress {self.id}>"
