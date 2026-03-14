from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'temporary_secret_key_for_admin_login'

db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Feedback {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    department = request.form.get('department')
    category = request.form.get('category')
    message = request.form.get('message')

    if not name or not email or not department or not category or not message:
        return "Missing fields", 400

    new_feedback = Feedback(
        name=name,
        email=email,
        department=department,
        category=category,
        message=message
    )
    db.session.add(new_feedback)
    db.session.commit()

    return redirect(url_for('success', id=new_feedback.id))

@app.route('/success')
def success():
    feedback_id = request.args.get('id')
    if not feedback_id:
        return redirect(url_for('home'))
        
    feedback = Feedback.query.get_or_404(feedback_id)
    return render_template('success.html', feedback=feedback)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    submissions = Feedback.query.order_by(Feedback.submitted_at.desc()).all()
    return render_template('admin.html', submissions=submissions)

@app.route('/update-status', methods=['POST'])
def update_status():
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    feedback_id = request.form.get('id')
    if not feedback_id:
        return jsonify({'success': False, 'message': 'Missing ID'}), 400
        
    feedback = Feedback.query.get(feedback_id)
    if feedback:
        feedback.status = 'Resolved'
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Feedback not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
