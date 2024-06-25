import os

class Settings:
    def __init__(self):
        self.HOST = os.getenv('HOST', 'localhost')
        self.PORT = os.getenv('PORT', 8000)
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'Hard_Too_Guest_2024')
        self.JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
        self.POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
        self.POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
        self.POSTGRES_DB = os.getenv('POSTGRES_DB', 'devOps')
        self.POSTGRES_SERVER = os.getenv('POSTGRES_SERVER', 'localhost')
        self.POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
        self.REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
        self.PROD = os.getenv('PROD', False)
        
        

# Create an instance of the Settings class
settings = Settings()
