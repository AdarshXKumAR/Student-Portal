# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from nldb import NLDatabaseInteractor
from functools import wraps

app = Flask(__name__)

# Configuration for MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'mysql'  
app.config['MYSQL_DB'] = 'user_auth_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Secret key for session
app.secret_key = os.urandom(24)

# Initialize MySQL
mysql = MySQL(app)

# Load environment variables
load_dotenv()

# Initialize NL Database Interactor with Gemini API
nldb_interactor = NLDatabaseInteractor(
    mysql=mysql, 
    api_key=os.getenv('GEMINI_API_KEY')
)

# Create database and tables if they don't exist
def init_db():
    try:
        # First connect without specifying a database
        app_config = {
            'MYSQL_HOST': app.config['MYSQL_HOST'],
            'MYSQL_USER': app.config['MYSQL_USER'],
            'MYSQL_PASSWORD': app.config['MYSQL_PASSWORD'],
            'MYSQL_CURSORCLASS': 'DictCursor'
        }
        
        import MySQLdb
        conn = MySQLdb.connect(
            host=app_config['MYSQL_HOST'],
            user=app_config['MYSQL_USER'],
            password=app_config['MYSQL_PASSWORD']
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS user_auth_db")
        cursor.execute("USE user_auth_db")
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                username VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create grades table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                subject VARCHAR(100) NOT NULL,
                score INT NOT NULL,
                grade CHAR(2) NOT NULL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database and tables created successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")

# Initialize database
init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please login to access this page', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nldb')
@login_required
def nldb_interface():
    return render_template('nldb.html')

@app.route('/nldb/query', methods=['POST'])
@login_required
def nldb_query():
    data = request.get_json()
    query = data.get('query', '')
    
    # Execute the natural language query
    result = nldb_interactor.execute_query(query)
    
    return jsonify(result)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form fields
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        # Create cursor
        cur = mysql.connection.cursor()

        # Check if username exists
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        if user:
            flash('Username already exists', 'danger')
            cur.close()
            return render_template('register.html')

        # Check if email exists
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        if user:
            flash('Email already exists', 'danger')
            cur.close()
            return render_template('register.html')

        # Hash password
        hashed_password = generate_password_hash(password)

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", 
                    (name, email, username, hashed_password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare passwords
            if check_password_hash(password, password_candidate):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = data['id']

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get user details
    cur.execute("SELECT * FROM users WHERE id = %s", [session['user_id']])
    user_data = cur.fetchone()

    # Get grades
    cur.execute("SELECT * FROM grades WHERE user_id = %s", [session['user_id']])
    grades = cur.fetchall()

    # Close connection
    cur.close()

    return render_template('dashboard.html', user_data=user_data, grades=grades)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Get form fields
        name = request.form['name']
        email = request.form['email']

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", 
                    (name, email, session['user_id']))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Profile updated', 'success')
        return redirect(url_for('dashboard'))

    # Create cursor
    cur = mysql.connection.cursor()

    # Get user details
    cur.execute("SELECT * FROM users WHERE id = %s", [session['user_id']])
    user_data = cur.fetchone()

    # Close connection
    cur.close()

    return render_template('profile.html', user_data=user_data)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        # Get form fields
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return render_template('change_password.html')

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by id
        cur.execute("SELECT * FROM users WHERE id = %s", [session['user_id']])
        user = cur.fetchone()

        # Check if old password is correct
        if not check_password_hash(user['password'], old_password):
            flash('Current password is incorrect', 'danger')
            cur.close()
            return render_template('change_password.html')

        # Hash new password
        hashed_password = generate_password_hash(new_password)

        # Execute query
        cur.execute("UPDATE users SET password = %s WHERE id = %s", 
                    (hashed_password, session['user_id']))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Password changed successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('change_password.html')

if __name__ == '__main__':
    app.run(debug=True)