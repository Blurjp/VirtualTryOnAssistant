import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    YOUR_AWS_ACCESS_KEY_ID = os.environ.get('YOUR_AWS_ACCESS_KEY_ID')
    YOUR_AWS_SECRET_ACCESS_KEY = os.environ.get('YOUR_AWS_SECRET_ACCESS_KEY')
    YOUR_AWS_REGION_NAME = 'us-east-1'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    S3_PROFILE_IMAGE_BUCKET_NAME = 'dev-fashion-assistant-user-image-profile-bucket'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'  # Change to the appropriate production database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    S3_PROFILE_IMAGE_BUCKET_NAME = 'prod-fashion-assistant-user-image-profile-bucket'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True