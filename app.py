from datetime import datetime

from flask import Flask

from config import Config
from models import Course, Lesson, Question, Quiz, User, db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from admin.routes import admin_bp
    from auth.routes import auth_bp
    from routes.main import main_bp
    from student.routes import student_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.utcnow().year}

    with app.app_context():
        db.create_all()
        seed_database()

    return app


def seed_database():
    admin_user = User.query.filter_by(email="admin@mamba.dev").first()
    if admin_user is None:
        admin_user = User(
            username="admin",
            email="admin@mamba.dev",
            role="admin",
        )
        admin_user.set_password("admin123")
        db.session.add(admin_user)

    if Course.query.count() > 0:
        db.session.commit()
        return

    python_course = Course(
        title="Python Foundations",
        description=(
            "Build strong Python fundamentals through practical lessons on syntax, "
            "functions, data structures, and real mini-projects."
        ),
    )
    frontend_course = Course(
        title="Frontend Essentials",
        description=(
            "Learn how HTML, CSS, Bootstrap, and JavaScript come together to build "
            "responsive interfaces that feel polished on every screen."
        ),
    )
    sql_course = Course(
        title="Data Thinking with SQL",
        description=(
            "Practice turning business questions into clean SQL queries, dashboards, "
            "and actionable product insights."
        ),
    )

    db.session.add_all([python_course, frontend_course, sql_course])
    db.session.flush()

    db.session.add_all(
        [
            Lesson(
                course_id=python_course.id,
                title="Variables and Flow Control",
                content=(
                    "Start with Python syntax, variables, conditionals, and loops. "
                    "By the end of this lesson you will be comfortable expressing "
                    "basic logic in readable Python code."
                ),
                video_url="https://www.youtube.com/embed/kqtD5dpn9C8",
            ),
            Lesson(
                course_id=python_course.id,
                title="Functions and Reusable Logic",
                content=(
                    "Understand function definitions, arguments, return values, and "
                    "how to structure scripts into reusable, testable building blocks."
                ),
                video_url="https://www.youtube.com/embed/NSbOtYzIQI0",
            ),
            Lesson(
                course_id=frontend_course.id,
                title="Responsive Layout Basics",
                content=(
                    "Explore semantic HTML, CSS layout patterns, and Bootstrap grid "
                    "techniques for building pages that adapt smoothly on mobile and desktop."
                ),
                video_url="https://www.youtube.com/embed/UB1O30fR-EE",
            ),
            Lesson(
                course_id=frontend_course.id,
                title="Interactive UI with JavaScript",
                content=(
                    "Use DOM events, stateful UI patterns, and progressive enhancement "
                    "to make interfaces dynamic without losing clarity."
                ),
                video_url="https://www.youtube.com/embed/W6NZfCO5SIk",
            ),
            Lesson(
                course_id=sql_course.id,
                title="Filtering and Aggregation",
                content=(
                    "Use WHERE, GROUP BY, COUNT, and SUM to answer common analytics "
                    "questions with confidence and accuracy."
                ),
                video_url="https://www.youtube.com/embed/HXV3zeQKqGY",
            ),
            Lesson(
                course_id=sql_course.id,
                title="Joins for Business Questions",
                content=(
                    "Learn how INNER JOIN and LEFT JOIN help you connect tables and "
                    "turn raw records into meaningful insight."
                ),
                video_url="https://www.youtube.com/embed/7S_tz1z_5bA",
            ),
        ]
    )

    db.session.add_all(
        [
            Quiz(course_id=python_course.id, title="Python Foundations Checkpoint"),
            Quiz(course_id=frontend_course.id, title="Frontend Essentials Checkpoint"),
            Quiz(course_id=sql_course.id, title="SQL Analytics Checkpoint"),
        ]
    )
    db.session.flush()

    quizzes = Quiz.query.all()
    quiz_by_course = {quiz.course_id: quiz for quiz in quizzes}

    db.session.add_all(
        [
            Question(
                quiz_id=quiz_by_course[python_course.id].id,
                question_text="Which keyword is used to define a function in Python?",
                options=["func", "define", "def", "lambda"],
                correct_answer="def",
            ),
            Question(
                quiz_id=quiz_by_course[python_course.id].id,
                question_text="Which structure is best for repeating logic a fixed number of times?",
                options=["for loop", "dictionary", "class", "import"],
                correct_answer="for loop",
            ),
            Question(
                quiz_id=quiz_by_course[frontend_course.id].id,
                question_text="Which Bootstrap class creates a responsive row container?",
                options=["container-row", "row", "grid", "col-auto"],
                correct_answer="row",
            ),
            Question(
                quiz_id=quiz_by_course[frontend_course.id].id,
                question_text="Which JavaScript method is commonly used to attach a click handler?",
                options=["queryClick", "addEventListener", "bindEvent", "setAction"],
                correct_answer="addEventListener",
            ),
            Question(
                quiz_id=quiz_by_course[sql_course.id].id,
                question_text="Which clause is used to combine rows from multiple tables?",
                options=["JOIN", "GROUP BY", "ORDER BY", "LIMIT"],
                correct_answer="JOIN",
            ),
            Question(
                quiz_id=quiz_by_course[sql_course.id].id,
                question_text="Which aggregate function counts rows?",
                options=["SUM", "AVG", "COUNT", "MAX"],
                correct_answer="COUNT",
            ),
        ]
    )

    db.session.commit()


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

