#!/usr/bin/env python3
"""
Advanced CT Scanner Preinstallation Verification System
Professional biomedical engineering solution with NeuViz support
"""

import os
import sys
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import openai
from dotenv import load_dotenv
from controllers.authentification import Authentication
from controllers.client import Client
from controllers.engineer import Engineer
from controllers.project import Project
from controllers.scanner_analysis import ScannerAnalysis
from controllers.report import ReportGenerator
from config import Config

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.config.from_object(Config)

# OpenAI setup
openai.api_key = os.getenv('OPENAI_API_KEY')

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ct_scanner_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize controllers
authentication = Authentication()
scanner_analysis = ScannerAnalysis()
report_generator = ReportGenerator()

# Utility function
def get_user_from_session():
    """Helper to get user info from session."""
    if 'user_id' in session and 'role' in session:
        return {'id': session['user_id'], 'role': session['role']}
    return None

def require_role(role):
    """Decorator to require specific user role."""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            user = get_user_from_session()
            if not user or user['role'] != role:
                flash(f'Access denied. {role.title()} privileges required.', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

# Routes
@app.route('/')
def index():
    """Main dashboard - shows different views based on user role."""
    user = get_user_from_session()
    if not user:
        return render_template('index.html')
    
    if user['role'] == 'client':
        return redirect(url_for('client_dashboard'))
    elif user['role'] == 'engineer':
        return redirect(url_for('engineer_dashboard'))
    elif user['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        role = request.form['role']
        email = request.form.get('email', '').strip()
        company = request.form.get('company', '').strip()
        
        if not username or not password or not role:
            flash('All required fields must be filled.', 'danger')
            return redirect(url_for('register'))
        
        success = authentication.register_user(username, password, role, email, company)
        if success:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed! Username may already exist.', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        role = request.form['role']
        
        user = authentication.login_user(username, password)
        if user and user['role'] == role:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['username'] = username
            flash(f'Welcome {username}!', 'success')
            
            if role == 'engineer':
                return redirect(url_for('engineer_dashboard'))
            elif role == 'client':
                return redirect(url_for('client_dashboard'))
            elif role == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials or role!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/client/dashboard')
@require_role('client')
def client_dashboard():
    """Client dashboard showing their projects."""
    user = get_user_from_session()
    client = Client()
    projects = client.get_user_projects(user['id'])
    return render_template('client_dashboard.html', projects=projects)

@app.route('/engineer/dashboard')
@require_role('engineer')
def engineer_dashboard():
    """Engineer dashboard showing assigned projects."""
    user = get_user_from_session()
    engineer = Engineer()
    projects = engineer.get_assigned_projects(user['id'])
    pending_analyses = engineer.get_pending_analyses()
    return render_template('engineer_dashboard.html', 
                         projects=projects, 
                         pending_analyses=pending_analyses)

@app.route('/admin/dashboard')
@require_role('admin')
def admin_dashboard():
    """Admin dashboard with system overview."""
    try:
        # Get system statistics
        with open('data/users.csv', 'r') as f:
            total_users = len(f.readlines()) - 1
    except:
        total_users = 0
    
    try:
        with open('data/projects.csv', 'r') as f:
            total_projects = len(f.readlines()) - 1
    except:
        total_projects = 0
    
    try:
        with open('data/analyses.csv', 'r') as f:
            total_analyses = len(f.readlines()) - 1
    except:
        total_analyses = 0
    
    stats = {
        'total_users': total_users,
        'total_projects': total_projects,
        'total_analyses': total_analyses,
        'ct_scanners': len(scanner_analysis.scanner_specs),
        'neuViz_scanners': sum(1 for model in scanner_analysis.scanner_specs if 'NeuViz' in model)
    }
    
    return render_template('admin_dashboard.html', stats=stats)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    """Create new CT scanner preinstallation project."""
    user = get_user_from_session()
    if not user:
        flash('Please login to create projects.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        project_data = {
            'client_id': user['id'],
            'project_name': request.form['project_name'],
            'facility_name': request.form['facility_name'],
            'contact_person': request.form['contact_person'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'scanner_model': request.form['scanner_model'],
            'installation_date': request.form['installation_date'],
            'notes': request.form.get('notes', '')
        }
        
        project = Project()
        project_id = project.create_project(project_data)
        
        if project_id:
            flash('Project created successfully!', 'success')
            return redirect(url_for('client_dashboard'))
        else:
            flash('Failed to create project.', 'danger')
    
    return render_template('project_new.html', 
                         scanner_models=scanner_analysis.scanner_specs.keys())

@app.route('/scanner/analysis/<int:project_id>', methods=['GET', 'POST'])
def scanner_analysis_page(project_id):
    """CT Scanner room analysis page."""
    user = get_user_from_session()
    if not user:
        flash('Please login to access scanner analysis.', 'danger')
        return redirect(url_for('login'))
    
    project = Project()
    project_data = project.get_project(project_id)
    
    if not project_data:
        flash('Project not found.', 'danger')
        return redirect(url_for('client_dashboard'))
    
    # Check permissions
    if user['role'] == 'client' and project_data['client_id'] != user['id']:
        flash('Access denied.', 'danger')
        return redirect(url_for('client_dashboard'))
    
    if request.method == 'POST':
        analysis_data = request.form.to_dict()
        analysis_data['project_id'] = project_id
        analysis_data['analyzer_id'] = user['id']
        
        result = scanner_analysis.analyze_room(analysis_data)
        
        if result:
            flash('Analysis completed successfully!', 'success')
            return render_template('analysis_results.html', 
                                 result=result, 
                                 project=project_data)
        else:
            flash('Analysis failed. Please try again.', 'danger')
    
    return render_template('scanner_analysis.html', 
                         project=project_data,
                         scanner_specs=scanner_analysis.scanner_specs)

@app.route('/reports/<int:project_id>')
def view_report(project_id):
    """View detailed report for a project."""
    user = get_user_from_session()
    if not user:
        flash('Please login to view reports.', 'danger')
        return redirect(url_for('login'))
    
    project = Project()
    project_data = project.get_project(project_id)
    
    if not project_data:
        flash('Project not found.', 'danger')
        return redirect(url_for('client_dashboard'))
    
    # Check permissions
    if user['role'] == 'client' and project_data['client_id'] != user['id']:
        flash('Access denied.', 'danger')
        return redirect(url_for('client_dashboard'))
    
    report = report_generator.generate_report(project_id)
    return render_template('report_view.html', report=report, project=project_data)

@app.route('/api/scanner-specs/<model>')
def get_scanner_specs(model):
    """API endpoint to get scanner specifications."""
    specs = scanner_analysis.scanner_specs.get(model)
    if specs:
        return jsonify(specs)
    return jsonify({'error': 'Scanner model not found'}), 404

@app.route('/api/analysis/dashboard', methods=['POST'])
def analysis_dashboard_api():
    """API endpoint for real-time analysis dashboard updates."""
    try:
        data = request.json
        dashboard_data = scanner_analysis.get_dashboard_metrics(data)
        return jsonify(dashboard_data)
    except Exception as e:
        logger.error(f"Dashboard API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/scanner/comparison', methods=['GET', 'POST'])
def scanner_comparison():
    """Compare multiple scanner models side by side."""
    comparisons = None
    if request.method == 'POST':
        selected = request.form.getlist('scanner_models')
        comparisons = scanner_analysis.compare_scanners(selected)
    return render_template('scanner_comparison.html',
                           scanner_models=scanner_analysis.scanner_specs.keys(),
                           comparisons=comparisons)

@app.route('/documentation/neuViz')
def neuViz_documentation():
    """NeuViz documentation page."""
    return render_template('neuViz_docs.html')

@app.route('/system/stats')
def system_stats():
    """System statistics page."""
    try:
        stats = scanner_analysis.get_system_statistics()
        return render_template('system_stats.html', stats=stats)
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        flash('Error loading statistics.', 'danger')
        return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {str(error)}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🚀 CT Scanner Pre-installation System")
    print("🔗 Starting locally at: http://localhost:5000")
    print("📊 Professional Biomedical Analysis Platform")
    print("=" * 50)
    
    try:
        app.run(host='127.0.0.1', port=5000, debug=False)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Make sure port 5000 is available")    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Create default admin user if not exists
    try:
        if not os.path.exists('data/users.csv'):
            authentication.create_default_admin()
    except Exception as e:
        logger.error(f"Error creating default admin: {e}")
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)