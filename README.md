# Student Feedback & Complaint Portal

A web portal where students can submit feedback or complaints. Developed with Flask, SQLite, Bootstrap 5, and jQuery.

## Features
- Student form with client-side validation using jQuery.
- SQLite database integration (creates database automatically).
- **Dark / Light Mode Table** that swaps themes instantly based on preference without page reloads.
- Protected Admin dashboard to view and manage submissions.
- Secure Session-Based Login Authentication for Admin panel.
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

## How to Use the Portal

### 1. Student Submission (Public)
1. Go to `http://localhost:5000` (Home Page)
2. Fill out the **Feedback & Complaint Form** with your details (Name, Email, Department, Category, and Message).
3. Ensure the message is at least 20 characters long.
4. Click **Submit**. You will be redirected to a green success screen displaying the details of your submission.

### 2. Admin Login & Dashboard
1. Click the **Admin** link in the navigation bar or go to `http://localhost:5000/admin`.
2. You will be prompted to log in:
   - **Username**: `admin`
   - **Password**: `admin123`
3. Click **Login** to enter the secure dashboard.
4. On the dashboard, you will see a list of all feedback and complaints.
5. Click **Mark Resolved** to instantly update the status of a pending request using AJAX (no page refresh).
6. Click **Logout** when finished.

### 3. Light / Dark Mode
Toggle the **Dark Mode** / **Light Mode** button in the top navigation bar to seamlessly switch themes!

## Folder structure overview
- `app.py`: Main Flask application and routes.
- `requirements.txt`: Python package dependencies.
- `static/`: Contains static assets like `css/style.css` and `js/script.js`.
- `templates/`: Contains HTML Jinja2 templates (`base.html`, `index.html`, `success.html`, `admin.html`).
- `database.db`: Auto-generated SQLite database.
