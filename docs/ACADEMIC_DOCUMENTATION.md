# Mamba Academic Project Documentation

## 1. Project Title

**Mamba: Full-Stack Educational Platform Using Flask**

## 2. Abstract

Mamba is a full-stack web-based educational platform developed using Python Flask. The system was designed to provide a complete online learning experience for students and a content management environment for administrators. The platform supports user registration and login, course browsing, course enrollment, lesson viewing, progress tracking, quiz solving, lesson comments, and course completion certificates. In addition, an admin dashboard enables the management of courses, lessons, quizzes, questions, and platform users.

This project demonstrates practical application of backend development, database design, frontend development, authentication, and deployment in a real-world educational use case.

## 3. Project Objective

The main objective of this project is to design and implement a modern educational platform that:

- allows students to access digital learning content in an organized way
- provides progress tracking and quiz assessment
- enables administrators to manage educational content efficiently
- demonstrates full-stack development using Flask and related technologies
- supports deployment to a live hosting environment

## 4. Problem Statement

Traditional learning environments often lack centralized systems that combine course browsing, lesson delivery, learner progress tracking, and simple administration tools in a single lightweight platform. The purpose of Mamba is to solve this by offering a practical e-learning solution that is easy to use, simple to manage, and suitable for small educational projects or academic demonstrations.

## 5. Scope of the Project

The scope of Mamba includes:

- student account creation and login
- course catalog and search
- lesson pages with text and embedded video support
- course enrollment and progress calculation
- quiz creation and submission
- basic learner interaction through comments
- certificate generation after course completion
- administrative control over courses and users

The project does not currently include:

- live video streaming
- payment integration
- email verification
- PDF certificate export
- advanced analytics or recommendation engines based on machine learning

## 6. Technologies Used

### Backend

- Python
- Flask
- Flask-Login
- Flask-WTF
- Flask-SQLAlchemy
- SQLAlchemy ORM

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Database

- SQLite for local development
- PostgreSQL-ready configuration for production deployment

### Deployment

- PythonAnywhere
- Render-ready setup included in the repository

## 7. System Architecture

The application follows a modular Flask architecture using Blueprints. Each major responsibility is separated into a dedicated module, which improves maintainability and scalability.

### Main Modules

- `routes/`
  Handles public pages such as the home page, course listing, and course details.

- `auth/`
  Handles registration, login, and logout.

- `student/`
  Handles student dashboard, enrollments, lessons, quizzes, progress, and certificates.

- `admin/`
  Handles content management including courses, lessons, quizzes, questions, and user viewing.

### Core Files

- [app.py](../app.py)
  Creates the Flask app, registers blueprints, initializes the database, and seeds demo data.

- [config.py](../config.py)
  Contains environment-based configuration for database and secret key setup.

- [models.py](../models.py)
  Defines all database models and relationships.

## 8. Functional Requirements

### Student Requirements

- register and log in securely
- browse all available courses
- search for courses
- enroll in a course
- access lessons in enrolled courses
- mark lessons as complete
- view progress percentage
- take quizzes and receive scores
- write comments under lessons
- open a course completion certificate

### Admin Requirements

- log in as administrator
- create, edit, and delete courses
- add and manage lessons
- create quizzes and questions
- view users
- preview content before student access

## 9. Non-Functional Requirements

- responsive user interface
- simple and clear navigation
- modular and maintainable code structure
- secure password handling
- role-based access control
- easy deployment to a live environment

## 10. Database Design

The database is designed using relational entities that represent users, educational content, progress tracking, and quiz activity.

### Entity Summary

#### User

- `id`
- `username`
- `email`
- `password_hash`
- `role`
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

## 11. System Workflow

### Student Workflow

1. A student creates an account or logs in.
2. The student browses or searches available courses.
3. The student enrolls in a selected course.
4. The student accesses lessons and studies the content.
5. After completing lessons, the student marks them as completed.
6. The system calculates progress automatically.
7. The student takes quizzes related to the course.
8. Quiz scores are stored in the database.
9. If all lessons are completed, the student can open the certificate page.

### Admin Workflow

1. The admin logs in using an admin account.
2. The admin accesses the dashboard.
3. The admin creates or edits courses.
4. The admin adds lessons and quizzes.
5. The admin creates quiz questions.
6. Published content becomes available to students.

## 12. Implemented Pages

- Home page
- Register page
- Login page
- Course catalog page
- Course details page
- Student dashboard
- Lesson page
- Quiz page
- Certificate page
- Admin dashboard
- Admin course editor
- Admin lesson editor
- Admin quiz editor
- Admin question editor
- User list page

## 13. Route Summary

### Public Routes

- `/`
- `/courses`
- `/courses/<course_id>`

### Authentication Routes

- `/register`
- `/login`
- `/logout`

### Student Routes

- `/student/dashboard`
- `/student/courses/<course_id>/enroll`
- `/student/courses/<course_id>/lessons/<lesson_id>`
- `/student/courses/<course_id>/lessons/<lesson_id>/complete`
- `/student/courses/<course_id>/quizzes/<quiz_id>`
- `/student/courses/<course_id>/certificate`

### Admin Routes

- `/admin/dashboard`
- `/admin/users`
- `/admin/courses/new`
- `/admin/courses/<course_id>/edit`
- `/admin/courses/<course_id>/delete`
- `/admin/courses/<course_id>/lessons/new`
- `/admin/lessons/<lesson_id>/edit`
- `/admin/lessons/<lesson_id>/delete`
- `/admin/courses/<course_id>/quizzes/new`
- `/admin/quizzes/<quiz_id>/edit`
- `/admin/quizzes/<quiz_id>/delete`
- `/admin/quizzes/<quiz_id>/questions/new`
- `/admin/questions/<question_id>/edit`
- `/admin/questions/<question_id>/delete`

## 14. Security and Validation

The project includes several security and validation mechanisms:

- passwords are hashed using Werkzeug security helpers
- user sessions are handled with Flask-Login
- private pages require authentication
- admin pages require role-based access control
- forms are validated using Flask-WTF and WTForms validators
- duplicate usernames and emails are prevented during registration

## 15. User Interface Design

The frontend was built using Bootstrap 5 with custom CSS to provide:

- a clean and modern landing page
- responsive design for desktop and mobile
- card-based course presentation
- progress bars for enrollment progress
- structured forms for authentication and admin input
- visually separated student and admin experiences

## 16. Testing and Verification

The project was tested through:

- route loading verification
- student flow testing:
  registration, enrollment, lesson access, lesson completion, quiz submission
- admin flow testing:
  login, dashboard access, course editing, quiz editing
- local runtime verification
- deployment verification on PythonAnywhere

## 17. Deployment

The project supports two deployment styles:

### PythonAnywhere

The project was successfully deployed on PythonAnywhere using:

- a virtual environment
- a WSGI configuration that imports `app` from `app.py`
- SQLite as the default database

### Render

The repository includes [render.yaml](../render.yaml), allowing deployment as a Flask web service with PostgreSQL support.

## 18. Default Admin Credentials

For demonstration purposes, the application seeds a default admin account:

- Email: `admin@mamba.dev`
- Password: `admin123`

## 19. Advantages of the Project

- complete full-stack implementation
- clean modular structure
- practical educational use case
- easy to run locally
- easy to demonstrate online
- strong portfolio and academic value

## 20. Limitations

- database migrations are not implemented yet
- SQLite is not ideal for large-scale production workloads
- comments are basic and do not include moderation
- certificates are HTML-based rather than downloadable PDFs
- there is no email verification or password reset workflow

## 21. Future Enhancements

- integrate Flask-Migrate for schema migrations
- add email verification
- add forgot-password support
- improve recommendation logic
- export certificates as PDF files
- add richer analytics for students and admins
- support media uploads for lessons
- introduce user profile customization

## 22. Conclusion

Mamba is a complete educational platform prototype that demonstrates how Flask can be used to build a full-stack academic project with real functionality. The project combines database design, authentication, content management, responsive frontend development, and cloud deployment in one integrated system.

This project is suitable as:

- a university project submission
- a portfolio project
- a foundation for future e-learning systems

## 23. References

- Flask Documentation
- Flask-Login Documentation
- Flask-WTF Documentation
- SQLAlchemy Documentation
- Bootstrap Documentation
- PythonAnywhere Documentation
- Render Documentation
