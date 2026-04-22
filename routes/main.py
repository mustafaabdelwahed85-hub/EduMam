import re

from flask import Blueprint, render_template, request
from flask_login import current_user
from sqlalchemy import or_

from models import Course
from student.forms import ActionForm


main_bp = Blueprint("main", __name__)


def tokenize(text):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def get_recommended_courses(user, limit=3):
    if not user.is_authenticated:
        return Course.query.order_by(Course.created_at.desc()).limit(limit).all()

    enrolled_ids = {enrollment.course_id for enrollment in user.enrollments}
    learner_keywords = set()

    for enrollment in user.enrollments:
        learner_keywords |= tokenize(enrollment.course.title)
        learner_keywords |= tokenize(enrollment.course.description)

    candidates = Course.query.all()
    ranked_courses = []
    for course in candidates:
        if course.id in enrolled_ids:
            continue

        keyword_score = len((tokenize(course.title) | tokenize(course.description)) & learner_keywords)
        popularity_score = course.enrolled_students
        freshness_score = int(course.created_at.timestamp()) if course.created_at else 0
        ranked_courses.append((keyword_score, popularity_score, freshness_score, course))

    ranked_courses.sort(key=lambda item: item[:3], reverse=True)
    return [item[3] for item in ranked_courses[:limit]]


@main_bp.route("/")
def home():
    featured_courses = Course.query.order_by(Course.created_at.desc()).limit(3).all()
    recommended_courses = get_recommended_courses(current_user, limit=3)
    return render_template(
        "home.html",
        featured_courses=featured_courses,
        recommended_courses=recommended_courses,
        enroll_form=ActionForm(),
    )


@main_bp.route("/courses")
def courses():
    query = request.args.get("q", "").strip()
    course_query = Course.query.order_by(Course.created_at.desc())

    if query:
        course_query = course_query.filter(
            or_(
                Course.title.ilike(f"%{query}%"),
                Course.description.ilike(f"%{query}%"),
            )
        )

    return render_template(
        "courses/list.html",
        courses=course_query.all(),
        query=query,
        enroll_form=ActionForm(),
    )


@main_bp.route("/courses/<int:course_id>")
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    enrollment = None
    if current_user.is_authenticated:
        enrollment = next(
            (item for item in current_user.enrollments if item.course_id == course.id),
            None,
        )

    related_courses = [item for item in get_recommended_courses(current_user, limit=4) if item.id != course.id][:3]

    return render_template(
        "courses/detail.html",
        course=course,
        enrollment=enrollment,
        related_courses=related_courses,
        enroll_form=ActionForm(),
    )
