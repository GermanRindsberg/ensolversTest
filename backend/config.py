class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "German"
   
    SESSION_COOKIE_SECURE = True

class DevelepmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///backend/database/tasks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

