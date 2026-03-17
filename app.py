from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and not session.get('admin_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'Admin':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'temporary_secret_key_for_admin_login'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='Student') # 'Student' or 'Admin'
    feedbacks = db.relationship('Feedback', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Nullable for legacy/guest feedback
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
    # Ensure instance folder exists
    if not os.path.exists(os.path.join(basedir, 'instance')):
        os.makedirs(os.path.join(basedir, 'instance'))
    db.create_all()

@app.route('/')
@login_required
def home():
    if session.get('role') == 'Admin':
        return redirect(url_for('admin'))
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    department = request.form.get('department')
    category = request.form.get('category')
    message = request.form.get('message')

    if not name or not email or not department or not category or not message:
        return "Missing fields", 400

    new_feedback = Feedback(
        user_id=session.get('user_id'),
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
    
    try:
        feedback_id = int(feedback_id)
    except ValueError:
        return redirect(url_for('home'))
        
    feedback = Feedback.query.get_or_404(feedback_id)
    return render_template('success.html', feedback=feedback)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username already exists")
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error="Email already exists")
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # Auto login after registration
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session['email'] = new_user.email
        session['role'] = new_user.role
        
        return redirect(url_for('home'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            session['role'] = user.role
            if user.role == 'Admin':
                session['admin_logged_in'] = True
                return redirect(url_for('admin'))
            return redirect(url_for('home'))
        
        # Fallback for old admin login
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            session['username'] = 'System Admin'
            session['role'] = 'Admin'
            # No user_id for system admin fallback
            return redirect(url_for('admin'))
            
        return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/my-feedbacks')
@login_required
def my_feedbacks():
    if not session.get('user_id'):
        return redirect(url_for('home'))
        
    user_feedbacks = Feedback.query.filter_by(user_id=session['user_id']).order_by(Feedback.submitted_at.desc()).all()
    return render_template('my_feedbacks.html', submissions=user_feedbacks)

@app.route('/admin')
@admin_required
def admin():
    submissions = Feedback.query.order_by(Feedback.submitted_at.desc()).all()
    return render_template('admin.html', submissions=submissions)

@app.route('/update-status', methods=['POST'])
@admin_required
def update_status():
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
