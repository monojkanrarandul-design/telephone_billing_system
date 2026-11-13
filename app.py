from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import random

app = Flask(__name__)
# Secret key is required to encrypt the session cookies securely
app.secret_key = 'getsuga_tenshou_secret' 
TARIFF_RATE = 1.50

def get_db_connection():
    conn = sqlite3.connect('telephone_billing_db.sqlite')
    conn.row_factory = sqlite3.Row  
    return conn

# Security Decorator: Forces users to log in before viewing specific pages
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- AUTHENTICATION ROUTES ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password) # Production standard security
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO SystemUser (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            error = "Username already exists!"
        finally:
            conn.close()
            
    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM SystemUser WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password"
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- CORE APPLICATION ROUTES ---

@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=session['username'])

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    bills = conn.execute('''
        SELECT b.bill_id, c.name, b.phone, b.call_duration, b.amount
        FROM Billing b
        JOIN Customer c ON b.phone = c.phone
        ORDER BY b.bill_id DESC
    ''').fetchall()
    conn.close()
    return render_template('dashboard.html', bills=bills)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_bill():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        call_duration = int(request.form['call_duration'])
        
        amount = call_duration * TARIFF_RATE

        conn = get_db_connection()
        conn.execute('INSERT OR IGNORE INTO Customer (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
        conn.execute('INSERT INTO Billing (phone, call_duration, amount) VALUES (?, ?, ?)', (phone, call_duration, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    
    return render_template('add_bill.html')

@app.route('/delete/<int:id>')
@login_required
def delete_bill(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Billing WHERE bill_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))
@app.route('/wipe_history')
@login_required
def wipe_history():
    conn= get_db_connection()
    #Delete all records from the billing table
    conn.execute('DELETE FROM Billing')
    #Reset the auto-inrement counter so the next Bill ID starts at 1
    conn.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = "Billing"')
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))
@app.route('/simulate_live_traffic')
@login_required
def simulate_live_traffic():
    # Roster of test subjects to simulate
    names = ["Kisuke Urahara", "Yoruichi Shihoin", "Byakuya Kuchiki", "Kenpachi Zaraki", "Grimmjow Jaegerjaquez", "Mayuri Kurotsuchi"]
    name = random.choice(names)
    
    # Generate random telecom data
    phone = f"98765{random.randint(10000, 99999)}"
    call_duration = random.randint(2, 85)
    amount = call_duration * TARIFF_RATE

    # Insert into database silently
    conn = get_db_connection()
    conn.execute('INSERT OR IGNORE INTO Customer (name, email, phone) VALUES (?, ?, ?)', (name, f"{name.split()[0].lower()}@sereitei.com", phone))
    cursor = conn.execute('INSERT INTO Billing (phone, call_duration, amount) VALUES (?, ?, ?)', (phone, call_duration, amount))
    new_bill_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Send the new data back to the dashboard instantly
    return jsonify({
        'bill_id': new_bill_id,
        'name': name,
        'phone': phone,
        'call_duration': call_duration,
        'amount': amount
    })
if __name__ == '__main__':
    app.run(debug=True)