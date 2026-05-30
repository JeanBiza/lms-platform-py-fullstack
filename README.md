# lms-platform

A fullstack Learning Management System (LMS) built with Flask and PostgreSQL, designed for internal corporate training.

> **Status:** In development

## Overview

Companies can use this platform to manage internal training courses, track employee progress, and issue completion certificates — without relying on third-party services.

**Admin (HR):** create courses and lessons, build quizzes, monitor progress across all employees, export reports.

**Employee:** browse and enroll in courses, complete lessons at their own pace, take quizzes, download certificates.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Flask |
| Database | PostgreSQL (Supabase) |
| ORM | Flask-SQLAlchemy + Flask-Migrate |
| Auth | Flask-Login |
| Email | Flask-Mail |
| PDF | ReportLab |
| Frontend | Jinja2, Bootstrap 5 |

## Project Structure

```
lms-platform/
├── app/
│   ├── __init__.py          # app factory
│   ├── extensions.py        # db, login_manager, mail
│   ├── models/              # SQLAlchemy models
│   ├── repositories/        # DB query layer
│   ├── routes/              # Flask blueprints
│   ├── services/            # business logic
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, JS, uploads
├── migrations/              # Alembic migrations
├── config.py
├── main.py
├── requirements.txt
└── .env.example
```

## Features

- **Auth & roles** — login system with `admin` and `employee` roles
- **Course catalog** — courses organized by category with lessons (video, PDF, text)
- **Progress tracking** — per-lesson completion, course progress percentage
- **Quizzes** — multiple choice with configurable passing score, unlimited retries
- **Certificates** — auto-generated PDF on course completion
- **Admin dashboard** — employee progress overview, filterable by department or course
- **Excel export** — training reports by date range

## Getting Started

```bash
git clone https://github.com/JeanBiza/lms-platform-py-fullstack.git
cd lms-platform-py-fullstack

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# fill in DATABASE_URL, SECRET_KEY, mail config

flask db upgrade
python main.py
```

## License

MIT
