import os
from dotenv import load_dotenv

# .env file load karo
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/foodheaven')
    DEBUG = True