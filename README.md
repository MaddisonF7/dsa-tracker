
# Digital Skills Academy Tracker

The Digital Skills Academy (DSA) Tracker is a Flask web application designed to help manage apprentices' journey throughout their apprenticeship. This includes viewing:
- All apprentices  
- All line managers  
- Exam progress  
- Previous and current projects  
- Tracking leave requests  

This document acts as a guide through the application's functionality, security design, and deployment best practices.

---

## Table of Contents
1. Overview  
2. Roles  
3. Installation  
4. Features  
5. Structure & Design  
6. Best Practices  
7. Security  
8. Deployment  
9. Known Limitations  

---

## 1. Overview
This application enables users to track and manage apprentices' progress and milestones within the Digital Skills Academy. The application consists of four tables:

### User:
- Stores both Apprentices and Admins.  
- Admins are line managers; apprentices are assigned a `line_manager_id`.  
- Uses hashed passwords for secure authentication.  
- Fields include: `email`, `password`, `first_name`, `last_name`, `role`, `line_manager_id`, `cohort`, `start_date`, `end_date`, `created_at`, and `modified_date`.

### Exam:
- Tracks exam attempts by apprentices.  
- Fields include: `id`, `name`, `exam_date`, `status`, `apprentice_id`, `created_at`, and `modified_date`.

### Leave_request:
- Manages leave status: pending, approved, or rejected.  
- Fields include: `id`, `apprentice_id`, `leave_type`, `start_date`, `end_date`, `status`, `created_at`, and `modified_date`.

### Project:
- Tracks apprentices’ current or past project assignments.  
- Fields include: `id`, `name`, `description`, `start_date`, `end_date`, `status`, `apprentice_id`, `created_at`, and `modified_date`.

---

## 2. Roles

### Admins:
- Line managers with full CRUD access to all tables.  
- Cannot change apprentice passwords.

### Apprentices:
- Can register, view, create, and update their own records.  
- Cannot delete any records or modify others' data.

---

## 3. Installation

### Prerequisites:
- Python 3.9+  
- MySQL Server  
- Flask  
- `requirements.txt` dependencies  

### Steps:
1. Clone the repository.  
2. Run `schema.sql` to set up the MySQL database.  
3. Configure DB credentials in `configuration.py`.  
4. Install packages: `pip install -r requirements.txt`  
5. Launch with: `python app.py`  
6. Access: `http://localhost:5000`

### Environment Setup:
Set a secure `SECRET_KEY` environment variable.

```bash
# Linux/macOS
export SECRET_KEY="your-secret-key"

# Windows
set SECRET_KEY="your-secret-key"
```

---

## 4. Features

### Users:
Admins manage all users. Apprentices manage only their own records.

### Exam:
Track progress and performance. Filtering included.

### Leave Requests:
Submit and track leave. Admins approve or reject.

### Projects:
Log and manage work placements or project tasks.

### Filtering:
Each tile supports dynamic filtering by name or field.

### Login & Register:
Users can register as either role. Sessions support secure logins.

---

## 5. Structure & Design

### Files:
- `app.py`: Launch point  
- `init.py`: Flask and DB config  
- `routes.py`: Route and logic definitions  
- `configuration.py`: Environment-based settings  
- `schema.sql`: DB table definitions
- `Dockerfile` Set up container

### Static:
- `styles.css`: UI styling  
- `script.js`: Form validation and UI features  

### Templates:
All routes use modular HTML files for views, e.g.:
- `login.html`, `exams.html`, `projects.html`, etc.

### Tests:
unittests
- `test_app.py`
- `test_apprentice.py`
- `test_exams.py`
- `test_home.py`
- `test_leave.py`
- `test_managers.py`
- `test_projects.py`
- `test_security.py`

### .gitHub/workflows:
- `heroku.yml` CI workflow
- `python-app.yml` CI workflow

---

## 6. Best Practices

### Modular Code:
App split into clean, testable modules.

### Secure Sessions:
- Sessions cleared on logout.  
- `SESSION_COOKIE_SECURE` enabled.  
- Session timeout via `PERMANENT_SESSION_LIFETIME`.

### Password Security:
- Passwords are hashed with Werkzeug before storage.  
- Validated using `check_password_hash()`.

### OWASP Awareness:
Defences implemented for:
- A02: Cryptographic Failures  
- A03: Injection  
- A07: Identification & Authentication Failures

---

## 7. Security

This application implements several OWASP-based protections:
- Passwords are stored as irreversible hashes.  
- SQL injection attempts are blocked through parameterised queries.  
- Session cookies are marked `Secure` and expire after inactivity.  
- Automated unit tests in `test_security.py` simulate login exploits, session hijacking, and credential leaks, all of which pass as expected.

---

## 8. Deployment

The app uses a GitHub-integrated CI/CD pipeline for deployment to Heroku.

- Repository: [MaddisonF7/dsa-tracker](https://github.com/MaddisonF7/dsa-tracker)  
- CI/CD Configs:
  - `python-app.yml`: Installs, lints, and tests on push to `main`.  
  - `heroku.yml`: Deploys to Heroku using CLI and GitHub Secrets.
- Database hosted on Heroku via JawsDB with connection string stored as an environment variable.
- Live deployment:  
  [https://digital-skills-academy-tracker-3e2c1cfbfbbe.herokuapp.com/](https://digital-skills-academy-tracker-3e2c1cfbfbbe.herokuapp.com/)

---

## 9. Known Limitations

- No MFA yet implemented.  
- No audit log or logging system for admin actions.  
- No real-time notifications or email integration for updates.
