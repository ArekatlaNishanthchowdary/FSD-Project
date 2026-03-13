# Student Feedback & Complaint Portal

A web portal where students can submit feedback or complaints. Developed with Flask, SQLite, Bootstrap 5, and jQuery.

## Features
- Student form with client-side validation using jQuery.
- SQLite database integration (creates database automatically).
- Secret Admin dashboard to view and manage submissions.
- AJAX-powered status updates.

## Technologies Used
- Flask
- Flask-SQLAlchemy (SQLite)
- HTML5, Bootstrap 5
- JavaScript (jQuery)

## Setup instructions
1. Clone the repo (or navigate to this directory)
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open http://localhost:5000 in your browser.

## How to access the admin page
Navigate to `http://localhost:5000/admin?password=admin123` to access the admin dashboard. 
From there, you can view all submissions and mark them as resolved.

## Folder structure overview
- `app.py`: Main Flask application and routes.
- `requirements.txt`: Python package dependencies.
- `static/`: Contains static assets like `css/style.css` and `js/script.js`.
- `templates/`: Contains HTML Jinja2 templates (`base.html`, `index.html`, `success.html`, `admin.html`).
- `database.db`: Auto-generated SQLite database.
