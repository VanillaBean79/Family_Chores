import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key for signing session cookies
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    # Session config
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_NAME = "session"

    # ✅ Important for React <-> Flask cookie sharing
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # must be False for http://localhost
    SESSION_COOKIE_HTTPONLY = True
