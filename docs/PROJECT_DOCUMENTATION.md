# Mamba Project Documentation

## 1. Project Overview

**Mamba** is a full-stack educational platform built with **Flask**. It allows students to register, explore courses, enroll in learning tracks, study lessons, take quizzes, track progress, and receive a completion certificate. The platform also includes an admin panel for managing courses, lessons, quizzes, questions, and users.

The project was designed to cover the full product flow of a learning platform, from authentication and database modeling to content management and deployment.

## 2. Main Features

### Student Features

- User registration and login
- Browse all available courses
- Search courses by title or description
- Enroll in courses
- Open lessons with text and embedded video support
- Mark lessons as complete
- Track progress per course
- Submit lesson comments
- Take quizzes and save quiz history
- View a completion certificate after finishing a course

### Admin Features

- Access a dedicated admin dashboard
- Create, edit, and delete courses
- Add, edit, and delete lessons
- Create quizzes for courses
- Add and manage quiz questions
- View platform users
- Preview content directly from admin pages

## 3. Technology Stack

- **Backend:** Python, Flask
- **Authentication:** Flask-Login
- **Forms and validation:** Flask-WTF, WTForms
- **Database ORM:** SQLAlchemy via Flask-SQLAlchemy
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Local database:** SQLite
- **Production database option:** PostgreSQL via `DATABASE_URL`
- **Production server:** Gunicorn
- **Deployment targets prepared:** Render and PythonAnywhere

## 4. Architecture

The project follows a modular structure using Flask Blueprints:

- `routes/` handles public pages such as home and course browsing
- `auth/` handles registration, login, and logout
- `student/` handles student-specific workflows
- `admin/` handles course and content management

The app is created in [app.py](../app.py), configuration lives in [config.py](../config.py), and database models are defined in [models.py](../models.py).

## 5. Project Structure

```text
EduMam/
├── admin/
│   ├── forms.py
│   └── routes.py
├── auth/
│   ├── forms.py
│   └── routes.py
├── docs/
│   └── PROJECT_DOCUMENTATION.md
├── routes/
│   └── main.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── student/
│   ├── forms.py
│   └── routes.py
├── templates/
│   ├── admin/
│   ├── auth/
│   ├── courses/
│   ├── partials/
│   └── student/
├── app.py
├── config.py
├── models.py
├── README.md
├── render.yaml
└── requirements.txt
```

## 6. Database Design

The application uses relational models to represent users, courses, content, enrollments, progress, and quiz activity.

### Models

#### User

- `id`
- `username`
- `email`
- `password_hash`
- `role` (`student` or `admin`)
- `created_at`

#### Course

- `id`
- `title`
- `description`
- `image`
- `created_at`

#### Lesson

- `id`
- `course_id`
- `title`
- `content`
- `video_url`
- `created_at`

#### Enrollment

- `id`
- `user_id`
- `course_id`
- `progress`
- `enrolled_at`

#### Quiz

- `id`
- `course_id`
- `title`

#### Question

- `id`
- `quiz_id`
- `question_text`
- `options`
- `correct_answer`

#### LessonProgress

- `id`
- `enrollment_id`
- `lesson_id`
- `completed_at`

#### LessonComment

- `id`
- `user_id`
- `lesson_id`
- `content`
- `created_at`

#### QuizSubmission

- `id`
- `user_id`
- `quiz_id`
- `score`
- `total_questions`
- `submitted_at`

## 7. Core Application Flow

### Student Flow

1. User creates an account or logs in
2. User opens the course catalog
3. User enrolls in a course
4. User studies lessons
5. User marks lessons as complete
6. The enrollment progress updates automatically
7. User submits a quiz
8. Quiz history is stored
9. Once all lessons are complete, the certificate becomes available

### Admin Flow

1. Admin logs in
2. Admin opens the dashboard
3. Admin creates or edits a course
4. Admin adds lessons
5. Admin creates quizzes and questions
6. Students can consume the published content immediately

## 8. Route Reference

### Public Routes

Defined in [routes/main.py](../routes/main.py)

- `/` : home page
- `/courses` : course catalog with search
- `/courses/<course_id>` : course details page

### Authentication Routes

Defined in [auth/routes.py](../auth/routes.py)

- `/register` : create a new student account
- `/login` : login page
- `/logout` : logout current user

### Student Routes

Defined in [student/routes.py](../student/routes.py)

- `/student/dashboard` : student dashboard
- `/student/courses/<course_id>/enroll` : enroll in a course
- `/student/courses/<course_id>/lessons/<lesson_id>` : lesson page
- `/student/courses/<course_id>/lessons/<lesson_id>/complete` : mark a lesson complete
- `/student/courses/<course_id>/quizzes/<quiz_id>` : quiz page
- `/student/courses/<course_id>/certificate` : certificate page

### Admin Routes

Defined in [admin/routes.py](../admin/routes.py)

- `/admin/dashboard` : admin dashboard
- `/admin/users` : list all users
- `/admin/courses/new` : create course
- `/admin/courses/<course_id>/edit` : edit course
- `/admin/courses/<course_id>/delete` : delete course
- `/admin/courses/<course_id>/lessons/new` : create lesson
- `/admin/lessons/<lesson_id>/edit` : edit lesson
- `/admin/lessons/<lesson_id>/delete` : delete lesson
- `/admin/courses/<course_id>/quizzes/new` : create quiz
- `/admin/quizzes/<quiz_id>/edit` : edit quiz
- `/admin/quizzes/<quiz_id>/delete` : delete quiz
- `/admin/quizzes/<quiz_id>/questions/new` : create question
- `/admin/questions/<question_id>/edit` : edit question
- `/admin/questions/<question_id>/delete` : delete question

## 9. Local Setup

### Prerequisites

- Python 3.13 or a compatible Python 3 version
- `pip`

### Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## 10. Configuration

Configuration is handled in [config.py](../config.py).

### Database Behavior

- If `DATABASE_URL` is not set, the app uses local SQLite with `mamba.db`
- If `DATABASE_URL` is provided, the app uses that database
- Render/Postgres URLs are normalized automatically for SQLAlchemy

### Important Environment Variables

- `SECRET_KEY`
- `DATABASE_URL`

## 11. Seed Data

On first startup, the application:

- creates the database tables with `db.create_all()`
- seeds demo courses, lessons, quizzes, and questions
- creates a default admin account if it does not exist

### Default Admin Credentials

- Email: `admin@mamba.dev`
- Password: `admin123`

## 12. Deployment Notes

### Render

The project includes [render.yaml](../render.yaml) for deployment with a web service and PostgreSQL database.

Manual settings:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

### PythonAnywhere

The project also runs successfully on PythonAnywhere using:

- a virtualenv
- the WSGI entry point `from app import app as application`
- SQLite by default

## 13. Security Notes

- Passwords are hashed using Werkzeug
- Admin access is restricted by role checks
- Forms use Flask-WTF validation
- Login protection is enforced on private student and admin pages

## 14. Known Limitations

- The project currently uses `db.create_all()` instead of migrations
- SQLite is suitable for demos and learning, but PostgreSQL is better for production
- Comments are simple text comments without moderation tools
- Certificate generation is currently HTML-based, not PDF-based

## 15. Suggested Future Improvements

- Add email verification
- Add password reset
- Add video upload support
- Add category filtering and tagging
- Add certificate PDF export
- Add analytics dashboard
- Add database migrations with Flask-Migrate
- Add test coverage for key student and admin flows

## 16. Troubleshooting

### `ModuleNotFoundError`

Install dependencies:

```bash
pip install -r requirements.txt
```

### App uses the wrong database

Check whether `DATABASE_URL` is set in the environment.

### Admin account not found

Restart the app once so `seed_database()` can run on startup.

### Static files not loading

Check the `static/` folder paths and verify Flask is serving the app from the project root.

## 17. Conclusion

Mamba is a complete educational platform prototype that demonstrates:

- modular Flask architecture
- user authentication
- content management
- relational database design
- responsive frontend implementation
- deployment readiness

It is suitable as a portfolio project, academic submission, or a strong starting point for a larger e-learning product.
