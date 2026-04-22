from datetime import datetime

from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Sign in to continue your Mamba journey."
login_manager.login_message_category = "warning"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    enrollments = db.relationship(
        "Enrollment",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    comments = db.relationship(
        "LessonComment",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    quiz_submissions = db.relationship(
        "QuizSubmission",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    lessons = db.relationship(
        "Lesson",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Lesson.id",
    )
    enrollments = db.relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan",
    )
    quizzes = db.relationship(
        "Quiz",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Quiz.id",
    )

    @property
    def total_lessons(self):
        return len(self.lessons)

    @property
    def enrolled_students(self):
        return len(self.enrollments)

    @property
    def average_progress(self):
        if not self.enrollments:
            return 0
        return int(sum(enrollment.progress for enrollment in self.enrollments) / len(self.enrollments))


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    course = db.relationship("Course", back_populates="lessons")
    comments = db.relationship(
        "LessonComment",
        back_populates="lesson",
        cascade="all, delete-orphan",
        order_by="desc(LessonComment.created_at)",
    )
    completions = db.relationship(
        "LessonProgress",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )


class Enrollment(db.Model):
    __table_args__ = (
        db.UniqueConstraint("user_id", "course_id", name="uq_user_course"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    progress = db.Column(db.Integer, nullable=False, default=0)
    enrolled_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")
    lesson_progress = db.relationship(
        "LessonProgress",
        back_populates="enrollment",
        cascade="all, delete-orphan",
    )

    def refresh_progress(self):
        total_lessons = len(self.course.lessons)
        if total_lessons == 0:
            self.progress = 100
            return self.progress

        completed_lessons = {item.lesson_id for item in self.lesson_progress}
        self.progress = int((len(completed_lessons) / total_lessons) * 100)
        return self.progress

    @property
    def is_complete(self):
        return self.progress >= 100


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)

    course = db.relationship("Course", back_populates="quizzes")
    questions = db.relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan",
        order_by="Question.id",
    )
    submissions = db.relationship(
        "QuizSubmission",
        back_populates="quiz",
        cascade="all, delete-orphan",
    )


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False, default=list)
    correct_answer = db.Column(db.String(255), nullable=False)

    quiz = db.relationship("Quiz", back_populates="questions")


class LessonProgress(db.Model):
    __table_args__ = (
        db.UniqueConstraint("enrollment_id", "lesson_id", name="uq_enrollment_lesson"),
    )

    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey("enrollment.id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    enrollment = db.relationship("Enrollment", back_populates="lesson_progress")
    lesson = db.relationship("Lesson", back_populates="completions")


class LessonComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="comments")
    lesson = db.relationship("Lesson", back_populates="comments")


class QuizSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    total_questions = db.Column(db.Integer, nullable=False, default=0)
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="quiz_submissions")
    quiz = db.relationship("Quiz", back_populates="submissions")


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

