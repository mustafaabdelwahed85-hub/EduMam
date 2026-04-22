# Mamba

Mamba is a Flask-based online learning platform with student and admin experiences.

## Features

- User registration and login
- Course catalog with search
- Lesson viewing with progress tracking
- Quizzes and score history
- Lesson comments
- Admin dashboard for managing courses, lessons, quizzes, questions, and users
- Course completion certificate
- SQLite locally and PostgreSQL on Render

## Documentation

Detailed project documentation is available in [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md).

## Run Locally

1. Create a virtual environment and activate it.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000`

## Database Setup

- Local development uses `mamba.db` automatically.
- Production deployment uses `DATABASE_URL` automatically.
- If `DATABASE_URL` points to Postgres, Mamba switches to PostgreSQL with SQLAlchemy.

## Deploy on Render

This repo now includes [render.yaml](render.yaml) so Render can create both:

- a Python web service for Flask
- a PostgreSQL database for Mamba

### Option 1: Blueprint deployment

1. Push this project to GitHub.
2. In Render, click `New` -> `Blueprint`.
3. Select your GitHub repo.
4. Render will detect `render.yaml` and propose:
   - `mamba-web`
   - `mamba-db`
5. Confirm creation and wait for the first deploy.

### Option 2: Manual deployment

If you create the web service manually instead of using the Blueprint:

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Runtime: `Python`
- Add environment variables:
  - `SECRET_KEY` = any strong secret
  - `DATABASE_URL` = your Render PostgreSQL internal connection string

### Notes

- On first boot, the app creates tables automatically with `db.create_all()`.
- Seed data is added automatically the first time the database is empty.
- Local SQLite remains available, so you can still run the app without Postgres on your machine.

## Default Admin Account

- Email: `admin@mamba.dev`
- Password: `admin123`
