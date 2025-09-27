import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLACHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    
    