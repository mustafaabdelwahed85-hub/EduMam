from functools import wraps

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from models import Course, Lesson, Question, Quiz, User, db

from .forms import ActionForm, CourseForm, LessonForm, QuestionForm, QuizForm


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if current_user.role != "admin":
            flash("Admin access only.", "danger")
            return redirect(url_for("student.dashboard"))
        return view_func(*args, **kwargs)

    return wrapped_view


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    courses = Course.query.order_by(Course.created_at.desc()).all()
    users = User.query.order_by(User.created_at.desc()).all()
    delete_form = ActionForm()

    stats = {
        "courses": Course.query.count(),
        "students": User.query.filter_by(role="student").count(),
        "admins": User.query.filter_by(role="admin").count(),
        "lessons": Lesson.query.count(),
        "quizzes": Quiz.query.count(),
    }

    return render_template(
        "admin/dashboard.html",
        courses=courses,
        users=users,
        stats=stats,
        delete_form=delete_form,
    )


@admin_bp.route("/users")
@login_required
@admin_required
def users_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/courses/new", methods=["GET", "POST"])
@login_required
@admin_required
def new_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            image=form.image.data.strip() if form.image.data else None,
        )
        db.session.add(course)
        db.session.commit()
        flash("Course created successfully.", "success")
        return redirect(url_for("admin.edit_course", course_id=course.id))

    return render_template("admin/course_form.html", form=form, course=None, delete_form=ActionForm())


@admin_bp.route("/courses/<int:course_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    delete_form = ActionForm()

    if form.validate_on_submit():
        course.title = form.title.data.strip()
        course.description = form.description.data.strip()
        course.image = form.image.data.strip() if form.image.data else None
        db.session.commit()
        flash("Course updated.", "success")
        return redirect(url_for("admin.edit_course", course_id=course.id))

    return render_template(
        "admin/course_form.html",
        form=form,
        course=course,
        delete_form=delete_form,
    )


@admin_bp.route("/courses/<int:course_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_course(course_id):
    form = ActionForm()
    if form.validate_on_submit():
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        flash("Course deleted.", "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/courses/<int:course_id>/lessons/new", methods=["GET", "POST"])
@login_required
@admin_required
def new_lesson(course_id):
    course = Course.query.get_or_404(course_id)
    form = LessonForm()

    if form.validate_on_submit():
        lesson = Lesson(
            course_id=course.id,
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            video_url=form.video_url.data.strip() if form.video_url.data else None,
        )
        db.session.add(lesson)
        db.session.commit()
        flash("Lesson added.", "success")
        return redirect(url_for("admin.edit_course", course_id=course.id))

    return render_template("admin/lesson_form.html", form=form, course=course, lesson=None, delete_form=ActionForm())


@admin_bp.route("/lessons/<int:lesson_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    form = LessonForm(obj=lesson)

    if form.validate_on_submit():
        lesson.title = form.title.data.strip()
        lesson.content = form.content.data.strip()
        lesson.video_url = form.video_url.data.strip() if form.video_url.data else None
        db.session.commit()
        flash("Lesson updated.", "success")
        return redirect(url_for("admin.edit_course", course_id=lesson.course_id))

    return render_template(
        "admin/lesson_form.html",
        form=form,
        course=lesson.course,
        lesson=lesson,
        delete_form=ActionForm(),
    )


@admin_bp.route("/lessons/<int:lesson_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_lesson(lesson_id):
    form = ActionForm()
    if form.validate_on_submit():
        lesson = Lesson.query.get_or_404(lesson_id)
        course_id = lesson.course_id
        db.session.delete(lesson)
        db.session.commit()
        flash("Lesson deleted.", "info")
        return redirect(url_for("admin.edit_course", course_id=course_id))
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/courses/<int:course_id>/quizzes/new", methods=["GET", "POST"])
@login_required
@admin_required
def new_quiz(course_id):
    course = Course.query.get_or_404(course_id)
    form = QuizForm()

    if form.validate_on_submit():
        quiz = Quiz(
            course_id=course.id,
            title=form.title.data.strip(),
        )
        db.session.add(quiz)
        db.session.commit()
        flash("Quiz created.", "success")
        return redirect(url_for("admin.edit_quiz", quiz_id=quiz.id))

    return render_template("admin/quiz_form.html", form=form, course=course, quiz=None, delete_form=ActionForm())


@admin_bp.route("/quizzes/<int:quiz_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizForm(obj=quiz)

    if form.validate_on_submit():
        quiz.title = form.title.data.strip()
        db.session.commit()
        flash("Quiz updated.", "success")
        return redirect(url_for("admin.edit_quiz", quiz_id=quiz.id))

    return render_template(
        "admin/quiz_form.html",
        form=form,
        course=quiz.course,
        quiz=quiz,
        delete_form=ActionForm(),
    )


@admin_bp.route("/quizzes/<int:quiz_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_quiz(quiz_id):
    form = ActionForm()
    if form.validate_on_submit():
        quiz = Quiz.query.get_or_404(quiz_id)
        course_id = quiz.course_id
        db.session.delete(quiz)
        db.session.commit()
        flash("Quiz deleted.", "info")
        return redirect(url_for("admin.edit_course", course_id=course_id))
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/quizzes/<int:quiz_id>/questions/new", methods=["GET", "POST"])
@login_required
@admin_required
def new_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()

    if form.validate_on_submit():
        question = Question(
            quiz_id=quiz.id,
            question_text=form.question_text.data.strip(),
            options=form.parsed_options(),
            correct_answer=form.correct_answer.data.strip(),
        )
        db.session.add(question)
        db.session.commit()
        flash("Question added.", "success")
        return redirect(url_for("admin.edit_quiz", quiz_id=quiz.id))

    return render_template(
        "admin/question_form.html",
        form=form,
        quiz=quiz,
        question=None,
        delete_form=ActionForm(),
    )


@admin_bp.route("/questions/<int:question_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    form = QuestionForm(obj=question)
    if not form.is_submitted():
        form.options_text.data = "\n".join(question.options or [])

    if form.validate_on_submit():
        question.question_text = form.question_text.data.strip()
        question.options = form.parsed_options()
        question.correct_answer = form.correct_answer.data.strip()
        db.session.commit()
        flash("Question updated.", "success")
        return redirect(url_for("admin.edit_quiz", quiz_id=question.quiz_id))

    return render_template(
        "admin/question_form.html",
        form=form,
        quiz=question.quiz,
        question=question,
        delete_form=ActionForm(),
    )


@admin_bp.route("/questions/<int:question_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_question(question_id):
    form = ActionForm()
    if form.validate_on_submit():
        question = Question.query.get_or_404(question_id)
        quiz_id = question.quiz_id
        db.session.delete(question)
        db.session.commit()
        flash("Question deleted.", "info")
        return redirect(url_for("admin.edit_quiz", quiz_id=quiz_id))
    return redirect(url_for("admin.dashboard"))

