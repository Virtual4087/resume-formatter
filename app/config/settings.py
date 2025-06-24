import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    # API Keys for Google Gemini API (supports multiple keys)
    GEMINI_API_KEYS = []
    if os.environ.get('GEMINI_API_KEYS'):
        GEMINI_API_KEYS = [key.strip() for key in os.environ.get('GEMINI_API_KEYS').split(',')]
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-please-change-in-production')
    DEBUG = False
    TESTING = False
    
    # File storage settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration dictionary to easily select the right configuration
config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig
}

def get_config(config_name='dev'):
    """Helper function to get configuration by name"""
    return config_by_name.get(config_name, DevelopmentConfig)