from flask import render_template, request, redirect, url_for, session, jsonify
from app import mongo
from bson import ObjectId
import hashlib
from datetime import datetime

def init_routes(app):
    
    # ==================== HOME PAGE ====================
    @app.route('/')
    def index():
        categories = list(mongo.categories.find({'is_active': True}))
        for cat in categories:
            cat['_id'] = str(cat['_id'])
        
        dishes = list(mongo.dishes.find({'is_available': True}).limit(6))
        for dish in dishes:
            dish['_id'] = str(dish['_id'])
        
        return render_template('index.html', categories=categories, featured_dishes=dishes)
    
    # ==================== MENU PAGE ====================
    @app.route('/menu')
    def menu():
        category_id = request.args.get('category')
        
        if category_id:
            dishes = list(mongo.dishes.find({'category_id': category_id, 'is_available': True}))
        else:
            dishes = list(mongo.dishes.find({'is_available': True}))
        
        categories = list(mongo.categories.find({'is_active': True}))
        
        for dish in dishes:
            dish['_id'] = str(dish['_id'])
        for cat in categories:
            cat['_id'] = str(cat['_id'])
        
        return render_template('menu.html', dishes=dishes, categories=categories, selected_category=category_id)
    
    # ==================== CART PAGE ====================
    @app.route('/cart')
    def cart():
        return render_template('cart.html')
    
    # ==================== CHECKOUT PAGE ====================
    @app.route('/checkout')
    def checkout():
        return render_template('checkout.html')
    
    # ==================== PLACE ORDER API ====================
    @app.route('/api/place-order', methods=['POST'])
    def place_order():
        try:
            data = request.json
            print(f"📦 Order received: {data}")
            
            user_id = session.get('user_id')
            order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            items = data.get('items', [])
            subtotal = sum(item.get('price', 0) for item in items)
            delivery_fee = 50
            packaging_fee = 20
            tax = int(subtotal * 0.05)
            total = subtotal + delivery_fee + packaging_fee + tax
            
            order_data = {
                'order_id': order_id,
                'user_id': user_id,
                'customer_name': data.get('name'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'delivery_address': data.get('address'),
                'special_instructions': data.get('instructions', ''),
                'items': items,
                'subtotal': subtotal,
                'delivery_fee': delivery_fee,
                'packaging_fee': packaging_fee,
                'tax': tax,
                'total_amount': total,
                'payment_method': 'Cash on Delivery',
                'status': 'pending',
                'order_date': datetime.now()
            }
            
            mongo.orders.insert_one(order_data)
            print(f"✅ Order saved: {order_id}")
            
            if user_id:
                mongo.users.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$push': {'orders': order_id}}
                )
            
            return jsonify({'success': True, 'order_id': order_id})
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # ==================== USER REGISTER ====================
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            password = request.form.get('password')
            
            if not all([name, email, phone, password]):
                return render_template('register.html', error='Please fill all fields! 📝')
            
            existing_user = mongo.users.find_one({'email': email})
            if existing_user:
                return render_template('register.html', error='Email already registered! 📧')
            
            user_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'password': hashlib.md5(password.encode()).hexdigest(),
                'role': 'user',
                'created_at': datetime.now(),
                'orders': []
            }
            
            mongo.users.insert_one(user_data)
            return redirect(url_for('login'))
        
        return render_template('register.html')
    
    # ==================== USER LOGIN ====================
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            if email and password:
                hashed_password = hashlib.md5(password.encode()).hexdigest()
                user = mongo.users.find_one({'email': email, 'password': hashed_password})
                
                if user:
                    session['user_id'] = str(user['_id'])
                    session['user_name'] = user.get('name', 'User')
                    session['user_role'] = user.get('role', 'user')
                    
                    if user.get('role') == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', error='Invalid email or password! ❌')
            else:
                return render_template('login.html', error='Please fill all fields! 📝')
        
        return render_template('login.html')
    
    # ==================== ADMIN LOGIN ====================
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            user = mongo.users.find_one({'email': email, 'password': hashed_password, 'role': 'admin'})
            
            if user:
                session['user_id'] = str(user['_id'])
                session['user_name'] = user.get('name', 'Admin')
                session['user_role'] = 'admin'
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('admin_login.html', error='Invalid admin credentials!')
        
        return render_template('admin_login.html')
    
    # ==================== ADMIN DASHBOARD ====================
    @app.route('/admin')
    def admin_dashboard():
        if not session.get('user_id') or session.get('user_role') != 'admin':
            return redirect(url_for('admin_login'))
        
        orders = list(mongo.orders.find().sort('order_date', -1))
        for order in orders:
            order['_id'] = str(order['_id'])
        
        stats = {
            'total_orders': mongo.orders.count_documents({}),
            'total_users': mongo.users.count_documents({'role': 'user'}),
            'total_revenue': sum(order.get('total_amount', 0) for order in mongo.orders.find()),
            'pending_orders': mongo.orders.count_documents({'status': 'pending'})
        }
        
        return render_template('admin/dashboard.html', orders=orders, stats=stats)
    
    # ==================== ADMIN UPDATE ORDER ====================
    @app.route('/admin/update-order/<order_id>', methods=['POST'])
    def update_order_status(order_id):
        if not session.get('user_id') or session.get('user_role') != 'admin':
            return jsonify({'error': 'Unauthorized'}), 401
        
        status = request.json.get('status')
        mongo.orders.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'status': status}}
        )
        
        return jsonify({'success': True})
    
    # ==================== ADMIN USERS PAGE ====================
    @app.route('/admin/users')
    def admin_users():
        if not session.get('user_id') or session.get('user_role') != 'admin':
            return redirect(url_for('admin_login'))
        
        users = list(mongo.users.find())
        for user in users:
            user['_id'] = str(user['_id'])
            user['order_count'] = mongo.orders.count_documents({'user_id': str(user['_id'])})
        
        return render_template('admin/users.html', users=users)
    
    # ==================== CREATE ADMIN USER ====================
    @app.route('/admin/setup')
    def setup_admin():
        existing_admin = mongo.users.find_one({'email': 'admin@foodheaven.com'})
        if not existing_admin:
            admin_data = {
                'name': 'Admin',
                'email': 'admin@foodheaven.com',
                'phone': '1234',
                'password': hashlib.md5('admin123'.encode()).hexdigest(),
                'role': 'admin',
                'created_at': datetime.now(),
                'orders': []
            }
            mongo.users.insert_one(admin_data)
            return "✅ Admin created!<br>Email: admin@foodheaven.com<br>Password: admin123<br><a href='/admin/login'>Click here to login</a>"
        else:
            return "⚠️ Admin already exists!<br><a href='/admin/login'>Click here to login</a>"
    
    # ==================== LOGOUT ====================
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))
    
    return app