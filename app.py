from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_development')
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'gayu_muthu_20')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'civicpulse')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Initialize MySQL
mysql = MySQL(app)

# Helper functions
def get_db_connection():
    return mysql.connection.cursor()

def execute_query(query, params=None, commit=False):
    cursor = get_db_connection()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    if commit:
        mysql.connection.commit()
        result = cursor.rowcount
    else:
        result = cursor.fetchall()
    
    cursor.close()
    return result

def is_logged_in(role=None):
    if 'logged_in' not in session:
        return False
    if role and session.get('role') != role:
        return False
    return True

# Routes
@app.route('/')
def index():
    avg_time_result = execute_query("""
        SELECT AVG(TIMESTAMPDIFF(HOUR, created_at, 
            (SELECT MIN(timestamp) FROM complaint_updates WHERE complaint_id = complaints.id AND status != 'New'))) as avg_time 
        FROM complaints
    """)[0]['avg_time']

    stats = {
        'issues_reported': execute_query("SELECT COUNT(*) as count FROM complaints")[0]['count'],
        'resolution_rate': execute_query("""
            SELECT ROUND((COUNT(CASE WHEN status = 'Resolved' THEN 1 END) / COUNT(*)) * 100, 0) as rate 
            FROM complaints
        """)[0]['rate'],
        'avg_response_time': round(avg_time_result) if avg_time_result is not None else 0,
        'partner_agencies': execute_query("SELECT COUNT(DISTINCT name) as count FROM departments")[0]['count']
    }

    recent_issues = execute_query("""
        SELECT id, title, status, created_at 
        FROM complaints 
        ORDER BY created_at DESC 
        LIMIT 5
    """)

    return render_template('index.html', stats=stats, recent_issues=recent_issues,now=datetime.now())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if role == 'User':
            user = execute_query("SELECT * FROM users WHERE email = %s", [email])
            if user and check_password_hash(user[0]['password'], password):
                session['logged_in'] = True
                session['user_id'] = user[0]['id']
                session['email'] = user[0]['email']
                session['name'] = user[0]['name']  # Store name in session
                session['role'] = 'User'
                return redirect(url_for('user_page'))
        else:
            # Authority login
            authority = execute_query("SELECT * FROM authorities WHERE email = %s", [email])
            if authority and check_password_hash(authority[0]['password'], password):
                session['logged_in'] = True
                session['authority_id'] = authority[0]['id']
                session['email'] = authority[0]['email']
                session['name'] = authority[0]['name']  # Store authority name
                session['role'] = 'Authority'
                return redirect(url_for('authority_dashboard'))
        
        flash('Invalid login credentials', 'danger')
    
    return render_template('login.html')

@app.route('/user-page')
def user_page():
    if not is_logged_in('User'):
        return redirect(url_for('login'))
    
    user_email = session.get('email')
    if not user_email:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))
    
    # Get user's complaints
    user_complaints = execute_query(
        "SELECT * FROM complaints WHERE contact_info = %s ORDER BY created_at DESC",
        [session['email']]
    )
    
    return render_template('user-page.html', 
                         name=session.get('name'),
                         complaints=user_complaints)

@app.route('/authority/dashboard')
def authority_dashboard():
    if not is_logged_in('Authority'):
        return redirect(url_for('login'))
    
    # Get dashboard statistics
    stats = {
        'total_complaints': execute_query("SELECT COUNT(*) as count FROM complaints")[0]['count'],
        'resolved': execute_query("SELECT COUNT(*) as count FROM complaints WHERE status = 'Resolved'")[0]['count'],
        'pending': execute_query("SELECT COUNT(*) as count FROM complaints WHERE status != 'Resolved'")[0]['count'],
        'departments': execute_query("SELECT COUNT(*) as count FROM departments")[0]['count']
    }
    
    # Get recent complaints
    recent_complaints = execute_query("""
        SELECT c.id, c.reference_id, c.title, c.status, c.created_at, d.name as department
        FROM complaints c
        LEFT JOIN departments d ON c.department_id = d.id
        ORDER BY c.created_at DESC
        LIMIT 10
    """)
    
    return render_template('dashboard.html',
                         name=session.get('name'),
                         stats=stats,
                         complaints=recent_complaints)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        # Check if email already exists
        if role == 'User':
            existing_user = execute_query("SELECT * FROM users WHERE email = %s", [email])
            if not existing_user:
                hashed_password = generate_password_hash(password)
                execute_query(
                    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, hashed_password),
                    commit=True
                )
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
        else:
            existing_user = execute_query("SELECT * FROM authorities WHERE email = %s", [email])
            if not existing_user:
                hashed_password = generate_password_hash(password)
                execute_query(
                    "INSERT INTO authorities (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, hashed_password),
                    commit=True
                )
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
        
        flash('Email already exists', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        # Process form data
        category = request.form['category']
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        landmark = request.form.get('landmark', '')
        contact = request.form.get('contact', '')
        
        # Handle image uploads
        images = []
        if 'images' in request.files:
            for file in request.files.getlist('images'):
                if file.filename:
                    # Save file and get path
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    images.append(file_path)
        
        # Save complaint to database
        complaint_id = execute_query(
            """INSERT INTO complaints 
               (title, description, category, location, landmark, contact_info, status) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (title, description, category, location, landmark, contact, 'New'),
            commit=True
        )
        
        # Save images if any
        for image_path in images:
            execute_query(
                "INSERT INTO complaint_images (complaint_id, image_path) VALUES (%s, %s)",
                (complaint_id, image_path),
                commit=True
            )
        
        # Add initial status update
        execute_query(
            """INSERT INTO complaint_updates 
               (complaint_id, status, message, timestamp) 
               VALUES (%s, %s, %s, NOW())""",
            (complaint_id, 'New', 'Complaint received and logged in the system.'),
            commit=True
        )
        
        # Generate reference ID
        reference_id = f"CMP-{datetime.now().year}-{complaint_id}"
        execute_query(
            "UPDATE complaints SET reference_id = %s WHERE id = %s",
            (reference_id, complaint_id),
            commit=True
        )
        
        flash(f'Your complaint has been submitted successfully. Your reference ID is {reference_id}', 'success')
        return redirect(url_for('track', complaint_id=reference_id))
    
    return render_template('report.html')

@app.route('/track', methods=['GET', 'POST'])
def track():
    complaint = None
    
    if request.method == 'POST':
        complaint_id = request.form['complaint_id']
        complaint = execute_query(
            "SELECT * FROM complaints WHERE reference_id = %s",
            [complaint_id]
        )
        
        if complaint:
            complaint = complaint[0]
            # Get timeline updates
            updates = execute_query(
                """SELECT * FROM complaint_updates 
                   WHERE complaint_id = %s 
                   ORDER BY timestamp DESC""",
                [complaint['id']]
            )
            complaint['updates'] = updates
            
            # Get images
            images = execute_query(
                "SELECT image_path FROM complaint_images WHERE complaint_id = %s",
                [complaint['id']]
            )
            complaint['images'] = [img['image_path'] for img in images]
    
    return render_template('track.html', complaint=complaint)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_logged_in('User'):
        return redirect(url_for('login'))
    
    # Get metrics for dashboard
    metrics = {
        'total_complaints': execute_query("SELECT COUNT(*) as count FROM complaints")[0]['count'],
        'resolved_issues': execute_query("SELECT COUNT(*) as count FROM complaints WHERE status = 'Resolved'")[0]['count'],
        'pending_issues': execute_query("SELECT COUNT(*) as count FROM complaints WHERE status != 'Resolved'")[0]['count'],
        'avg_resolution_time': execute_query("""
            SELECT AVG(TIMESTAMPDIFF(DAY, created_at, 
                (SELECT MAX(timestamp) FROM complaint_updates 
                 WHERE complaint_id = complaints.id AND status = 'Resolved'))) as avg_time 
            FROM complaints 
            WHERE status = 'Resolved'
        """)[0]['avg_time']
    }
    
    # Get complaints for table
    complaints = execute_query("""
        SELECT c.id, c.reference_id, c.title, c.category, c.status, c.priority, DATE_FORMAT(c.created_at, '%Y-%m-%d') as date
        FROM complaints c
        ORDER BY c.created_at DESC
        LIMIT 50
    """)
    
    # Get data for charts
    category_data = execute_query("""
        SELECT category, COUNT(*) as count 
        FROM complaints 
        GROUP BY category
    """)
    
    trend_data = execute_query("""
        SELECT 
            DATE_FORMAT(c.created_at, '%Y-%m') as month,
            AVG(TIMESTAMPDIFF(DAY, c.created_at, 
                (SELECT MAX(timestamp) FROM complaint_updates 
                 WHERE complaint_id = c.id AND status = 'Resolved'))) as avg_time
        FROM complaints c
        WHERE c.status = 'Resolved'
        GROUP BY DATE_FORMAT(c.created_at, '%Y-%m')
        ORDER BY month
        LIMIT 6
    """)
    
    status_data = execute_query("""
        SELECT 
            d.name as department,
            COUNT(CASE WHEN c.status = 'New' THEN 1 END) as new_count,
            COUNT(CASE WHEN c.status = 'Assigned' THEN 1 END) as assigned_count,
            COUNT(CASE WHEN c.status = 'In Progress' THEN 1 END) as in_progress_count,
            COUNT(CASE WHEN c.status = 'Resolved' THEN 1 END) as resolved_count
        FROM complaints c
        JOIN departments d ON c.department_id = d.id
        GROUP BY d.name
    """)
    
    return render_template(
        'dashboard.html', 
        metrics=metrics, 
        complaints=complaints,
        category_data=json.dumps([{'name': c['category'], 'value': c['count']} for c in category_data]),
        trend_data=json.dumps([{'month': t['month'], 'value': float(t['avg_time'] or 0)} for t in trend_data]),
        status_data=json.dumps([{
            'department': s['department'],
            'new': s['new_count'],
            'assigned': s['assigned_count'],
            'in_progress': s['in_progress_count'],
            'resolved': s['resolved_count']
        } for s in status_data])
    )

@app.route('/admin/complaint/<complaint_id>')
def admin_complaint_detail(complaint_id):
    if not is_logged_in('Authority'):
        return redirect(url_for('login'))
    
    complaint = execute_query(
        "SELECT * FROM complaints WHERE id = %s",
        [complaint_id]
    )
    
    if complaint:
        complaint = complaint[0]
        # Get timeline updates
        updates = execute_query(
            """SELECT * FROM complaint_updates 
               WHERE complaint_id = %s 
               ORDER BY timestamp DESC""",
            [complaint['id']]
        )
        complaint['updates'] = updates
        
        # Get images
        images = execute_query(
            "SELECT image_path FROM complaint_images WHERE complaint_id = %s",
            [complaint['id']]
        )
        complaint['images'] = [img['image_path'] for img in images]
    
    return render_template('admin_complaint_detail.html', complaint=complaint)

@app.route('/admin/update_complaint', methods=['POST'])
def admin_update_complaint():
    if not is_logged_in('Authority'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    complaint_id = request.form['complaint_id']
    status = request.form['status']
    message = request.form['message']
    
    # Update complaint status
    execute_query(
        "UPDATE complaints SET status = %s, updated_at = NOW() WHERE id = %s",
        (status, complaint_id),
        commit=True
    )
    
    # Add status update
    execute_query(
        """INSERT INTO complaint_updates 
           (complaint_id, status, message, timestamp) 
           VALUES (%s, %s, %s, NOW())""",
        (complaint_id, status, message),
        commit=True
    )
    
    return jsonify({'success': True})

@app.route('/api/complaints')
def api_complaints():
    if not is_logged_in('Authority'):
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    department = request.args.get('department')
    search = request.args.get('search', '')
    
    query = """
        SELECT c.id, c.reference_id, c.title, c.category, c.status, c.priority, 
               DATE_FORMAT(c.created_at, '%Y-%m-%d') as date
        FROM complaints c
        JOIN departments d ON c.department_id = d.id
        WHERE 1=1
    """
    params = []
    
    if department and department != 'All Departments':
        query += " AND d.name = %s"
        params.append(department)
    
    if search:
        query += " AND (c.title LIKE %s OR c.reference_id LIKE %s OR c.description LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])
    
    query += " ORDER BY c.created_at DESC LIMIT 50"
    
    complaints = execute_query(query, params)
    
    return jsonify({'success': True, 'data': complaints})

if __name__ == '__main__':
    app.run(debug=True)

