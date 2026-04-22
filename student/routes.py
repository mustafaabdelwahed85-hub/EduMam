import re
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import (
    Course,
    Enrollment,
    Lesson,
    LessonComment,
    LessonProgress,
    Quiz,
    QuizSubmission,
    db,
)

from .forms import ActionForm, CommentForm


student_bp = Blueprint("student", __name__, url_prefix="/student")


def learner_recommendations(user, limit=3):
    enrolled_ids = {enrollment.course_id for enrollment in user.enrollments}
    keywords = set(re.findall(r"[a-z0-9]+", " ".join(enrollment.course.title for enrollment in user.enrollments).lower()))

    ranked = []
    for course in Course.query.all():
        if course.id in enrolled_ids:
            continue
        course_keywords = set(re.findall(r"[a-z0-9]+", f"{course.title} {course.description}".lower()))
        score = len(course_keywords & keywords) + course.enrolled_students
        ranked.append((score, course.created_at or datetime.utcnow(), course))

    ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [item[2] for item in ranked[:limit]]


def get_user_enrollment(course_id):
    return Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()


@student_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "admin":
        return redirect(url_for("admin.dashboard"))

    enrollments = (
        Enrollment.query.filter_by(user_id=current_user.id)
        .order_by(Enrollment.enrolled_at.desc())
        .all()
    )
    submissions = (
        QuizSubmission.query.filter_by(user_id=current_user.id)
        .order_by(QuizSubmission.submitted_at.desc())
        .limit(5)
        .all()
    )
    recommended_courses = learner_recommendations(current_user, limit=3)

    return render_template(
        "student/dashboard.html",
        enrollments=enrollments,
        submissions=submissions,
        recommended_courses=recommended_courses,
        enroll_form=ActionForm(),
    )


@student_bp.route("/courses/<int:course_id>/enroll", methods=["POST"])
@login_required
def enroll_course(course_id):
    form = ActionForm()
    if not form.validate_on_submit():
        flash("Your session expired. Please try again.", "warning")
        return redirect(url_for("main.course_detail", course_id=course_id))

    course = Course.query.get_or_404(course_id)
    if current_user.role == "admin":
        flash("Admins can browse courses without enrolling.", "info")
        return redirect(url_for("main.course_detail", course_id=course.id))

    existing_enrollment = get_user_enrollment(course.id)
    if existing_enrollment:
        flash("You are already enrolled in this course.", "info")
        return redirect(url_for("student.dashboard"))

    enrollment = Enrollment(user=current_user, course=course)
    db.session.add(enrollment)
    enrollment.refresh_progress()
    db.session.commit()

    flash(f"You are now enrolled in {course.title}.", "success")
    return redirect(url_for("student.dashboard"))


@student_bp.route("/courses/<int:course_id>/lessons/<int:lesson_id>", methods=["GET", "POST"])
@login_required
def lesson_page(course_id, lesson_id):
    course = Course.query.get_or_404(course_id)
    lesson = Lesson.query.get_or_404(lesson_id)

    if lesson.course_id != course.id:
        flash("That lesson does not belong to this course.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))

    enrollment = None
    if current_user.role != "admin":
        enrollment = get_user_enrollment(course.id)
        if enrollment is None:
            flash("Enroll in the course to unlock lessons.", "warning")
            return redirect(url_for("main.course_detail", course_id=course.id))

    comment_form = CommentForm()
    complete_form = ActionForm()

    if comment_form.validate_on_submit():
        comment = LessonComment(
            user_id=current_user.id,
            lesson_id=lesson.id,
            content=comment_form.content.data.strip(),
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment added.", "success")
        return redirect(url_for("student.lesson_page", course_id=course.id, lesson_id=lesson.id))

    lesson_ids = [item.id for item in course.lessons]
    lesson_index = lesson_ids.index(lesson.id)
    previous_lesson = course.lessons[lesson_index - 1] if lesson_index > 0 else None
    next_lesson = course.lessons[lesson_index + 1] if lesson_index < len(course.lessons) - 1 else None

    completed_lesson_ids = set()
    if enrollment:
        completed_lesson_ids = {item.lesson_id for item in enrollment.lesson_progress}

    return render_template(
        "student/lesson.html",
        course=course,
        lesson=lesson,
        enrollment=enrollment,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
        completed_lesson_ids=completed_lesson_ids,
        comment_form=comment_form,
        complete_form=complete_form,
    )


@student_bp.route("/courses/<int:course_id>/lessons/<int:lesson_id>/complete", methods=["POST"])
@login_required
def complete_lesson(course_id, lesson_id):
    form = ActionForm()
    if not form.validate_on_submit():
        flash("Your session expired. Please try again.", "warning")
        return redirect(url_for("student.lesson_page", course_id=course_id, lesson_id=lesson_id))

    course = Course.query.get_or_404(course_id)
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.course_id != course.id:
        flash("That lesson does not belong to this course.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))

    enrollment = get_user_enrollment(course.id)
    if enrollment is None:
        flash("Enroll first to track progress.", "warning")
        return redirect(url_for("main.course_detail", course_id=course.id))

    already_completed = LessonProgress.query.filter_by(
        enrollment_id=enrollment.id,
        lesson_id=lesson.id,
    ).first()
    if already_completed is None:
        progress_entry = LessonProgress(enrollment=enrollment, lesson=lesson)
        db.session.add(progress_entry)
        db.session.flush()
        enrollment.refresh_progress()
        db.session.commit()
        flash("Lesson marked as complete.", "success")
    else:
        flash("You already completed this lesson.", "info")

    return redirect(url_for("student.lesson_page", course_id=course.id, lesson_id=lesson.id))


@student_bp.route("/courses/<int:course_id>/quizzes/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def quiz_page(course_id, quiz_id):
    course = Course.query.get_or_404(course_id)
    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.course_id != course.id:
        flash("That quiz does not belong to this course.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))

    enrollment = None
    if current_user.role != "admin":
        enrollment = get_user_enrollment(course.id)
        if enrollment is None:
            flash("Enroll in the course before taking the quiz.", "warning")
            return redirect(url_for("main.course_detail", course_id=course.id))

    score = None
    submitted_answers = {}

    if request.method == "POST":
        submitted_answers = {
            str(question.id): request.form.get(f"question_{question.id}", "")
            for question in quiz.questions
        }
        score = sum(
            1
            for question in quiz.questions
            if submitted_answers.get(str(question.id)) == question.correct_answer
        )

        if current_user.role != "admin":
            submission = QuizSubmission(
                user_id=current_user.id,
                quiz_id=quiz.id,
                score=score,
                total_questions=len(quiz.questions),
            )
            db.session.add(submission)
            db.session.commit()

        flash(f"You scored {score}/{len(quiz.questions)} on {quiz.title}.", "success")

    latest_submission = None
    if current_user.role != "admin":
        latest_submission = (
            QuizSubmission.query.filter_by(user_id=current_user.id, quiz_id=quiz.id)
            .order_by(QuizSubmission.submitted_at.desc())
            .first()
        )

    return render_template(
        "student/quiz.html",
        course=course,
        quiz=quiz,
        enrollment=enrollment,
        score=score,
        submitted_answers=submitted_answers,
        latest_submission=latest_submission,
    )


@student_bp.route("/courses/<int:course_id>/certificate")
@login_required
def certificate(course_id):
    course = Course.query.get_or_404(course_id)
    enrollment = get_user_enrollment(course.id)
    if enrollment is None:
        flash("Enroll in the course first.", "warning")
        return redirect(url_for("main.course_detail", course_id=course.id))

    enrollment.refresh_progress()
    db.session.commit()

    if not enrollment.is_complete:
        flash("Complete all lessons to unlock your certificate.", "warning")
        return redirect(url_for("student.dashboard"))

    return render_template(
        "student/certificate.html",
        course=course,
        enrollment=enrollment,
        issued_on=datetime.utcnow(),
    )
