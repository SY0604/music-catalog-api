import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfiguration:
    """Database connection and configuration settings."""
    
    def __init__(self):
        self.mongodb_connection = os.getenv("MONGODB_CONNECTION", "mongodb://localhost:27017")
        self.database_name = os.getenv("DATABASE_NAME", "musicdb")
