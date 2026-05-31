from app.extensions import db

class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    course = db.relationship("Course", back_populates="lessons")

    title = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer , nullable=False)
    type = db.Column(db.String(256), nullable=False)
    content = db.Column(db.String(500), nullable=False) 

    lesson_progress = db.relationship("LessonProgress", back_populates="lesson")

    def __repr__(self):
        return f"<Lesson {self.title}>"
