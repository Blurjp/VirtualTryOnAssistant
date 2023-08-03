import os
from config import DevelopmentConfig, ProductionConfig, TestingConfig

def get_config():
    env = os.getenv('CONFIG_ENV', 'development')
    if env == 'development':
        return DevelopmentConfig()
    elif env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        raise ValueError("Invalid environment name")
