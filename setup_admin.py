from app import create_app
from datetime import datetime
import hashlib

print("=" * 50)
print("👑 Creating Admin User...")
print("=" * 50)

# Create app
app = create_app()

# Use app context
with app.app_context():
    from app import mongo
    
    # Check if mongo is connected
    if mongo is None:
        print("❌ MongoDB is not connected!")
        print("Please check:")
        print("1. MongoDB service is running")
        print("2. .env file has correct MONGO_URI")
        print("3. MongoDB Compass can connect to localhost:27017")
        exit()
    
    print("✅ MongoDB connected!")
    
    # Check if users collection exists, if not create it
    if 'users' not in mongo.list_collection_names():
        mongo.create_collection('users')
        print("✅ Created 'users' collection")
    
    # Check if admin exists
    existing = mongo.users.find_one({'email': 'admin@foodheaven.com'})
    
    if existing:
        print("⚠️ Admin already exists!")
        print(f"   Email: admin@foodheaven.com")
        print(f"   Password: admin123")
        print(f"   Name: {existing.get('name')}")
    else:
        # Create admin user
        admin_data = {
            'name': 'Super Admin',
            'email': 'admin@foodheaven.com',
            'phone': '9876543210',
            'password': hashlib.md5('admin123'.encode()).hexdigest(),
            'role': 'admin',
            'is_active': True,
            'created_at': datetime.now(),
            'orders': []
        }
        
        result = mongo.users.insert_one(admin_data)
        print("✅ Admin created successfully!")
        print(f"   Email: admin@foodheaven.com")
        print(f"   Password: admin123")
        print(f"   ID: {result.inserted_id}")
    
    print("\n" + "=" * 50)
    print("🔗 Admin Login URL:")
    print("   http://localhost:5000/admin/login")
    print("=" * 50)