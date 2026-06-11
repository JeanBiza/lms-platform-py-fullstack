# lms-platform
 
A fullstack Learning Management System (LMS) built with Flask and PostgreSQL, designed for internal corporate training.
 
> **Status:** ✅ Functional — core features complete
 
## Overview
 
Companies use this platform to manage internal training courses, track employee progress, and issue completion certificates — without relying on third-party services.
 
**Admin (HR):** create and manage courses, lessons, and quizzes. Monitor employee progress across all courses. Manage users and roles.
 
**Employee:** browse and enroll in courses, complete lessons, take quizzes, download certificates.
 
## Features
 
- **Auth & roles** — login, register, logout with `admin` and `employee` roles
- **Course management** — full CRUD with active/inactive toggle and cascade delete
- **Lessons** — support for video (YouTube embed), PDF, and text content types
- **Progress tracking** — per-lesson completion with progress bar
- **Quiz system** — multiple choice with configurable passing score, lesson gate (must complete all lessons first), attempt history
- **Certificates** — auto-generated PDF on course completion (ReportLab)
- **Employee dashboard** — enrolled courses, progress overview, quick actions
- **Admin dashboard** — employee progress table, recent enrollments, stats
- **User management** — create users, toggle roles (admin/employee), delete accounts
## Tech Stack
 
| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12+, Flask |
| Database | PostgreSQL |
| ORM | Flask-SQLAlchemy + Flask-Migrate |
| Auth | Flask-Login |
| PDF | ReportLab |
| Frontend | Jinja2, Bootstrap 5 |
 
## Project Structure
 
```
lms_app/
├── app/
│   ├── __init__.py          # app factory
│   ├── extensions.py        # db, login_manager, migrate
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── lesson.py
│   │   ├── quiz.py
│   │   ├── question.py
│   │   ├── option.py
│   │   ├── enrollment.py
│   │   ├── lesson_progress.py
│   │   ├── quiz_attempt.py
│   │   └── quiz_answer.py
│   ├── routes/              # Flask blueprints
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── courses.py
│   │   ├── lessons.py
│   │   ├── employee.py
│   │   ├── quiz.py
│   │   └── admin.py
│   ├── services/
│   │   └── certificate_service.py
│   ├── templates/           # Jinja2 HTML templates
│   └── static/
├── migrations/              # Alembic migrations
├── config.py
├── main.py
├── seed.py                  # default admin user
├── requirements.txt
└── .env.example
```
 
## Getting Started
 
### 1. Clone the repo
 
```bash
git clone https://github.com/JeanBiza/lms-platform-py-fullstack.git
cd lms-platform-py-fullstack
```
 
### 2. Create and activate virtual environment
 
```bash
python -m venv venv
 
# Linux / macOS
source venv/bin/activate
 
# Windows
venv\Scripts\activate
```
 
### 3. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4. Configure environment variables
 
```bash
cp .env.example .env
```
 
Edit `.env` and fill in:
 
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/your_db_name
```
 
### 5. Create the database
 
Create a PostgreSQL database (via pgAdmin, DBeaver, or psql):
 
```sql
CREATE DATABASE <YOUR_DATABASE_NAME>;
```
 
### 6. Run migrations
 
```bash
flask db upgrade
```
 
### 7. Create default admin user
 
```bash
python seed.py
```
 
This creates an admin user with:
- **Email:** `admin`
- **Password:** `admin`
> ⚠️ Change the admin credentials immediately after first login via the Users panel.
 
### 8. Run the app
 
```bash
python main.py
```
 
Visit `http://localhost:5000`
 
## Environment Variables
 
| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key for sessions |
| `DATABASE_URL` | PostgreSQL connection string |
 
## Default Workflows
 
### Admin
1. Login with default admin credentials
2. Go to **Users** → create your own admin account → delete default admin
3. Go to **Courses** → create courses and add lessons
4. Add a quiz to each course with questions and options
5. Monitor employee progress from the **Dashboard**
### Employee
1. Register or get an account from admin
2. Browse the **Catalog** and enroll in courses
3. Complete lessons in order
4. Take the quiz once all lessons are done
5. Download the **Certificate** on completion
## License
 
MIT
 