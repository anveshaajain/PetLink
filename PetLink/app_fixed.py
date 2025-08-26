from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'petlink_secret_key_2024'

# Database initialization
def init_db():
    try:
        conn = sqlite3.connect('petlink.db')
        cursor = conn.cursor()
        
        # Create Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                contact TEXT NOT NULL,
                address TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Owners table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS owners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                contact TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Create Pets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER,
                breed TEXT NOT NULL,
                age INTEGER NOT NULL,
                health_details TEXT,
                medical_details TEXT,
                adoption_status TEXT DEFAULT 'available',
                image_url TEXT,
                owner_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id),
                FOREIGN KEY (owner_id) REFERENCES owners (id)
            )
        ''')
        
        # Create Adoption Requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS adoption_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                pet_id INTEGER,
                status TEXT DEFAULT 'pending',
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (pet_id) REFERENCES pets (id)
            )
        ''')
        
        # Insert default categories
        categories = ['Dogs', 'Cats', 'Birds', 'Others']
        for category in categories:
            cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (category,))
        
        # Insert default owner
        default_owner_password = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO owners (name, email, password, contact) 
            VALUES (?, ?, ?, ?)
        ''', ('Admin Owner', 'admin@petlink.com', default_owner_password, '+1234567890'))
        
        # Insert sample pets
        sample_pets = [
            ('Buddy', 1, 'Golden Retriever', 3, 'Healthy and energetic', 'Vaccinated, neutered', 'available', 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=400', 1),
            ('Luna', 2, 'Persian', 2, 'Calm and friendly', 'Vaccinated, spayed', 'available', 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400', 1),
            ('Max', 1, 'German Shepherd', 4, 'Well-trained guard dog', 'All vaccinations up to date', 'available', 'https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?w=400', 1),
            ('Whiskers', 2, 'Maine Coon', 1, 'Playful kitten', 'First vaccinations done', 'available', 'https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400', 1),
            ('Charlie', 3, 'Cockatiel', 2, 'Loves to sing', 'Healthy, no medical issues', 'available', 'https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=400', 1),
            ('Bella', 1, 'Labrador', 5, 'Great with kids', 'Vaccinated, microchipped', 'available', 'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=400', 1),
            ('Mittens', 2, 'Siamese', 3, 'Independent but loving', 'Vaccinated, spayed', 'available', 'https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400', 1),
            ('Rocky', 1, 'Bulldog', 6, 'Gentle giant', 'Regular health checkups', 'available', 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400', 1),
            ('Tweety', 3, 'Canary', 1, 'Beautiful singer', 'Healthy and active', 'available', 'https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400', 1),
            ('Shadow', 4, 'Rabbit', 2, 'Quiet and gentle', 'Vaccinated, litter trained', 'available', 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400', 1)
        ]
        
        for pet in sample_pets:
            cursor.execute('''
                INSERT OR IGNORE INTO pets (name, category_id, breed, age, health_details, medical_details, adoption_status, image_url, owner_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', pet)
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Database initialization error: {e}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    conn = sqlite3.connect('petlink.db')
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/')
def home():
    try:
        conn = get_db_connection()
        pets = conn.execute('''
            SELECT p.*, c.name as category_name 
            FROM pets p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.adoption_status = "available" 
            LIMIT 6
        ''').fetchall()
        conn.close()
        return render_template('index.html', pets=pets)
    except Exception as e:
        print(f"Home route error: {e}")
        return f"Error: {e}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = hash_password(request.form['password'])
            contact = request.form['contact']
            address = request.form['address']
            
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO users (name, email, password, contact, address)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, password, contact, address))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')
        except Exception as e:
            flash(f'Registration error: {e}', 'error')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = hash_password(request.form['password'])
            
            conn = get_db_connection()
            user = conn.execute(
                'SELECT * FROM users WHERE email = ? AND password = ?',
                (email, password)
            ).fetchone()
            conn.close()
            
            if user:
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_type'] = 'user'
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password!', 'error')
        except Exception as e:
            flash(f'Login error: {e}', 'error')
    
    return render_template('login.html')

@app.route('/owner-login', methods=['GET', 'POST'])
def owner_login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = hash_password(request.form['password'])
            
            conn = get_db_connection()
            owner = conn.execute(
                'SELECT * FROM owners WHERE email = ? AND password = ?',
                (email, password)
            ).fetchone()
            conn.close()
            
            if owner:
                session['user_id'] = owner['id']
                session['user_name'] = owner['name']
                session['user_type'] = 'owner'
                flash('Owner login successful!', 'success')
                return redirect(url_for('owner_dashboard'))
            else:
                flash('Invalid email or password!', 'error')
        except Exception as e:
            flash(f'Owner login error: {e}', 'error')
    
    return render_template('owner_login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user_id' not in session or session.get('user_type') != 'user':
        flash('Please login to access your profile.', 'error')
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        
        # Get user's adoption requests
        requests = conn.execute('''
            SELECT ar.*, p.name as pet_name, p.breed, c.name as category_name
            FROM adoption_requests ar
            JOIN pets p ON ar.pet_id = p.id
            JOIN categories c ON p.category_id = c.id
            WHERE ar.user_id = ?
            ORDER BY ar.created_at DESC
        ''', (session['user_id'],)).fetchall()
        
        conn.close()
        return render_template('profile.html', user=user, requests=requests)
    except Exception as e:
        flash(f'Profile error: {e}', 'error')
        return redirect(url_for('home'))

@app.route('/adopt')
def adopt():
    try:
        category_filter = request.args.get('category', '')
        
        conn = get_db_connection()
        
        # Get all categories
        categories = conn.execute('SELECT * FROM categories').fetchall()
        
        # Build query based on filter
        if category_filter:
            pets = conn.execute('''
                SELECT p.*, c.name as category_name 
                FROM pets p 
                JOIN categories c ON p.category_id = c.id 
                WHERE p.adoption_status = "available" AND c.name = ?
                ORDER BY p.created_at DESC
            ''', (category_filter,)).fetchall()
        else:
            pets = conn.execute('''
                SELECT p.*, c.name as category_name 
                FROM pets p 
                JOIN categories c ON p.category_id = c.id 
                WHERE p.adoption_status = "available"
                ORDER BY p.created_at DESC
            ''').fetchall()
        
        conn.close()
        return render_template('adopt.html', pets=pets, categories=categories, selected_category=category_filter)
    except Exception as e:
        return f"Adopt page error: {e}"

@app.route('/request-adoption/<int:pet_id>', methods=['POST'])
def request_adoption(pet_id):
    if 'user_id' not in session or session.get('user_type') != 'user':
        return jsonify({'success': False, 'message': 'Please login to request adoption.'})
    
    try:
        data = request.get_json()
        message = data.get('message', '') if data else ''
        
        conn = get_db_connection()
        
        # Check if user already requested this pet
        existing = conn.execute(
            'SELECT * FROM adoption_requests WHERE user_id = ? AND pet_id = ?',
            (session['user_id'], pet_id)
        ).fetchone()
        
        if existing:
            conn.close()
            return jsonify({'success': False, 'message': 'You have already requested this pet.'})
        
        # Create adoption request
        conn.execute('''
            INSERT INTO adoption_requests (user_id, pet_id, message)
            VALUES (?, ?, ?)
        ''', (session['user_id'], pet_id, message))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Adoption request submitted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/owner-dashboard')
def owner_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'owner':
        flash('Please login as owner to access dashboard.', 'error')
        return redirect(url_for('owner_login'))
    
    try:
        conn = get_db_connection()
        
        # Get owner's pets
        pets = conn.execute('''
            SELECT p.*, c.name as category_name 
            FROM pets p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.owner_id = ?
            ORDER BY p.created_at DESC
        ''', (session['user_id'],)).fetchall()
        
        # Get adoption requests
        requests = conn.execute('''
            SELECT ar.*, p.name as pet_name, p.breed, u.name as user_name, u.email, u.contact
            FROM adoption_requests ar
            JOIN pets p ON ar.pet_id = p.id
            JOIN users u ON ar.user_id = u.id
            WHERE p.owner_id = ?
            ORDER BY ar.created_at DESC
        ''', (session['user_id'],)).fetchall()
        
        categories = conn.execute('SELECT * FROM categories').fetchall()
        
        conn.close()
        return render_template('owner_dashboard.html', pets=pets, requests=requests, categories=categories)
    except Exception as e:
        return f"Owner dashboard error: {e}"

@app.route('/add-pet', methods=['POST'])
def add_pet():
    if 'user_id' not in session or session.get('user_type') != 'owner':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO pets (name, category_id, breed, age, health_details, medical_details, image_url, owner_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['category_id'], data['breed'], data['age'],
            data['health_details'], data['medical_details'], data['image_url'], session['user_id']
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Pet added successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/update-pet/<int:pet_id>', methods=['POST'])
def update_pet(pet_id):
    if 'user_id' not in session or session.get('user_type') != 'owner':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        conn.execute('''
            UPDATE pets SET name = ?, category_id = ?, breed = ?, age = ?, 
            health_details = ?, medical_details = ?, image_url = ?, adoption_status = ?
            WHERE id = ? AND owner_id = ?
        ''', (
            data['name'], data['category_id'], data['breed'], data['age'],
            data['health_details'], data['medical_details'], data['image_url'],
            data['adoption_status'], pet_id, session['user_id']
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Pet updated successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/delete-pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    if 'user_id' not in session or session.get('user_type') != 'owner':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM pets WHERE id = ? AND owner_id = ?', (pet_id, session['user_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Pet deleted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/update-request-status/<int:request_id>', methods=['POST'])
def update_request_status(request_id):
    if 'user_id' not in session or session.get('user_type') != 'owner':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    try:
        data = request.get_json()
        status = data.get('status')
        
        conn = get_db_connection()
        
        # Update request status
        conn.execute('UPDATE adoption_requests SET status = ? WHERE id = ?', (status, request_id))
        
        # If approved, update pet status
        if status == 'approved':
            request_info = conn.execute(
                'SELECT pet_id FROM adoption_requests WHERE id = ?', (request_id,)
            ).fetchone()
            if request_info:
                conn.execute(
                    'UPDATE pets SET adoption_status = "adopted" WHERE id = ?',
                    (request_info['pet_id'],)
                )
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Request {status} successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})

@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    if 'user_id' not in session or session.get('user_type') != 'user':
        return jsonify({'success': False, 'message': 'Please login to delete your profile.'})
    
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if not password:
            return jsonify({'success': False, 'message': 'Password is required to delete your profile.'})
        
        # Verify password
        hashed_password = hash_password(password)
        
        conn = get_db_connection()
        
        # Check if password is correct
        user = conn.execute(
            'SELECT * FROM users WHERE id = ? AND password = ?',
            (session['user_id'], hashed_password)
        ).fetchone()
        
        if not user:
            conn.close()
            return jsonify({'success': False, 'message': 'Incorrect password. Profile deletion cancelled.'})
        
        user_id = session['user_id']
        user_name = user['name']
        
        # Delete all adoption requests by this user
        conn.execute('DELETE FROM adoption_requests WHERE user_id = ?', (user_id,))
        
        # Delete the user account
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        # Clear session
        session.clear()
        
        return jsonify({
            'success': True, 
            'message': f'Profile deleted successfully. Goodbye {user_name}! You can register again anytime with the same credentials.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error deleting profile: {e}'})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🐾 Starting PetLink Application...")
    print("Initializing database...")
    init_db()
    print("Database ready!")
    print("\n" + "="*50)
    print("🌐 PetLink is running!")
    print("📍 Main site: http://localhost:5000")
    print("🔑 Owner login: http://localhost:5000/owner-login")
    print("📧 Demo owner: admin@petlink.com / admin123")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)