from app.extensions import db
import datetime


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text , nullable=False)
    category = db.Column(db.String(256), nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=False) 
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    lessons = db.relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    quiz = db.relationship("Quiz", back_populates="course", uselist=False, cascade="all, delete-orphan")
    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course {self.title}>"