from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///naijatechhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    skills = db.Column(db.String(500), default='')
    location = db.Column(db.String(100), default='Lagos')
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    saved_opportunities = db.relationship('SavedOpportunity', backref='user', lazy=True)

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills_required = db.Column(db.String(500), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    apply_link = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SavedOpportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

def get_recommendations(user_skills, limit=6):
    if not user_skills:
        return Opportunity.query.filter_by(is_active=True).order_by(Opportunity.views.desc()).limit(limit).all()
    user_skill_list = [s.strip().lower() for s in user_skills.split(',')]
    opportunities = Opportunity.query.filter_by(is_active=True).all()
    scored_opps = []
    for opp in opportunities:
        opp_skills = [s.strip().lower() for s in opp.skills_required.split(',')]
        match_score = sum(1 for skill in user_skill_list if skill in opp_skills)
        scored_opps.append((opp, match_score))
    scored_opps.sort(key=lambda x: x[1], reverse=True)
    return [opp for opp, score in scored_opps[:limit]]

@app.route('/')
def home():
    featured = Opportunity.query.filter_by(is_active=True).order_by(Opportunity.views.desc()).limit(6).all()
    recent = Opportunity.query.filter_by(is_active=True).order_by(Opportunity.created_at.desc()).limit(4).all()
    return render_template('home.html', featured=featured, recent=recent)

@app.route('/opportunities')
def opportunities():
    page = request.args.get('page', 1, type=int)
    type_filter = request.args.get('type', '')
    location_filter = request.args.get('location', '')
    query = Opportunity.query.filter_by(is_active=True)
    if type_filter:
        query = query.filter_by(type=type_filter)
    if location_filter:
        query = query.filter(Opportunity.location.contains(location_filter))
    all_opps = query.order_by(Opportunity.created_at.desc()).paginate(page=page, per_page=12, error_out=False)
    return render_template('opportunities.html', opportunities=all_opps, type_filter=type_filter, location_filter=location_filter)

@app.route('/opportunity/<int:id>')
def opportunity_detail(id):
    opp = Opportunity.query.get_or_404(id)
    opp.views += 1
    db.session.commit()
    is_saved = False
    if 'user_id' in session:
        is_saved = SavedOpportunity.query.filter_by(user_id=session['user_id'], opportunity_id=id).first() is not None
    return render_template('opportunity_detail.html', opportunity=opp, is_saved=is_saved)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        skills = request.form['skills']
        location = request.form['location']
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        user = User(name=name, email=email, password_hash=generate_password_hash(password), skills=skills, location=location)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash('Welcome back, ' + user.name + '!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    saved = SavedOpportunity.query.filter_by(user_id=user.id).all()
    recommendations = get_recommendations(user.skills)
    return render_template('dashboard.html', user=user, saved=saved, recommendations=recommendations)

@app.route('/save-opportunity/<int:id>')
def save_opportunity(id):
    if 'user_id' not in session:
        flash('Please login to save opportunities!', 'warning')
        return redirect(url_for('login'))
    existing = SavedOpportunity.query.filter_by(user_id=session['user_id'], opportunity_id=id).first()
    if not existing:
        saved = SavedOpportunity(user_id=session['user_id'], opportunity_id=id)
        db.session.add(saved)
        db.session.commit()
        flash('Opportunity saved!', 'success')
    else:
        flash('Already saved!', 'info')
    return redirect(url_for('opportunity_detail', id=id))

@app.route('/admin')
def admin_dashboard():
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('home'))
    total_users = User.query.count()
    total_opps = Opportunity.query.count()
    total_saved = SavedOpportunity.query.count()
    recent_opps = Opportunity.query.order_by(Opportunity.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', total_users=total_users, total_opps=total_opps, total_saved=total_saved, recent_opps=recent_opps)

@app.route('/admin/add-opportunity', methods=['GET', 'POST'])
def add_opportunity():
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('Access denied!', 'danger')
        return redirect(url_for('home'))
    if request.method == 'POST':
        opp = Opportunity(title=request.form['title'], company=request.form['company'], type=request.form['type'], location=request.form['location'], description=request.form['description'], skills_required=request.form['skills_required'], deadline=datetime.strptime(request.form['deadline'], '%Y-%m-%d').date(), apply_link=request.form['apply_link'])
        db.session.add(opp)
        db.session.commit()
        flash('Opportunity added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/add_opportunity.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)