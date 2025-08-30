from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///campus_connect.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=True)
    year_of_study = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    events_created = db.relationship('Event', backref='creator', lazy=True)
    study_groups_created = db.relationship('StudyGroup', backref='creator', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=False)  # academic, social, sports, etc.
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class StudyGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    max_members = db.Column(db.Integer, default=10)
    meeting_time = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Many-to-many relationship for members
    members = db.relationship('User', secondary='study_group_members', backref='study_groups')

# Association table for study group members
study_group_members = db.Table('study_group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('study_group_id', db.Integer, db.ForeignKey('study_group.id'), primary_key=True)
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    recent_events = Event.query.filter(Event.is_active == True).order_by(Event.date.desc()).limit(5).all()
    active_groups = StudyGroup.query.filter(StudyGroup.is_active == True).limit(5).all()
    return render_template('index.html', events=recent_events, groups=active_groups)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        full_name = request.form['full_name']
        course = request.form.get('course', '')
        year_of_study = request.form.get('year_of_study', '')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            course=course,
            year_of_study=int(year_of_study) if year_of_study else None
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful!')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('User not found')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/events')
def events():
    category = request.args.get('category', 'all')
    if category == 'all':
        events = Event.query.filter(Event.is_active == True).order_by(Event.date.desc()).all()
    else:
        events = Event.query.filter(Event.category == category, Event.is_active == True).order_by(Event.date.desc()).all()
    
    return render_template('events.html', events=events, current_category=category)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date_str = request.form['date']
        time = request.form['time']
        location = request.form['location']
        category = request.form['category']
        
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        event = Event(
            title=title,
            description=description,
            date=event_date,
            time=time,
            location=location,
            category=category,
            creator_id=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash('Event created successfully!')
        return redirect(url_for('events'))
    
    return render_template('create_event.html')

@app.route('/study_groups')
def study_groups():
    subject = request.args.get('subject', 'all')
    if subject == 'all':
        groups = StudyGroup.query.filter(StudyGroup.is_active == True).all()
    else:
        groups = StudyGroup.query.filter(StudyGroup.subject.contains(subject), StudyGroup.is_active == True).all()
    
    return render_template('study_groups.html', groups=groups, current_subject=subject)

@app.route('/create_study_group', methods=['GET', 'POST'])
@login_required
def create_study_group():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        description = request.form['description']
        max_members = int(request.form['max_members'])
        meeting_time = request.form['meeting_time']
        location = request.form['location']
        
        group = StudyGroup(
            name=name,
            subject=subject,
            description=description,
            max_members=max_members,
            meeting_time=meeting_time,
            location=location,
            creator_id=current_user.id
        )
        
        # Add creator as first member
        group.members.append(current_user)
        
        db.session.add(group)
        db.session.commit()
        
        flash('Study group created successfully!')
        return redirect(url_for('study_groups'))
    
    return render_template('create_study_group.html')

@app.route('/join_study_group/<int:group_id>')
@login_required
def join_study_group(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    
    if current_user in group.members:
        flash('You are already a member of this group')
    elif len(group.members) >= group.max_members:
        flash('This study group is full')
    else:
        group.members.append(current_user)
        db.session.commit()
        flash('Successfully joined the study group!')
    
    return redirect(url_for('study_groups'))

@app.route('/leave_study_group/<int:group_id>')
@login_required
def leave_study_group(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    
    if current_user in group.members:
        group.members.remove(current_user)
        db.session.commit()
        flash('You have left the study group')
    
    return redirect(url_for('study_groups'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Get port from environment variable (Render uses PORT)
    port = int(os.environ.get('PORT', 5000))
    # Disable debug in production
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
