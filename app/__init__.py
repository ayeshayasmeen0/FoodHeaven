from flask import Flask
from pymongo import MongoClient
from config import Config

mongo = None

def create_app():
    global mongo
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Secret key for sessions
    app.secret_key = app.config['SECRET_KEY']
    
    # MongoDB connection
    client = MongoClient(app.config['MONGO_URI'])
    mongo = client.get_database('foodheaven')
    
    # Test connection
    try:
        client.admin.command('ping')
        print("✅ MongoDB connected!")
    except Exception as e:
        print(f"❌ MongoDB error: {e}")
    
    # Import routes
    from app.routes import init_routes
    init_routes(app)
    
    return app