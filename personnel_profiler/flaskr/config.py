
username = "postgres"
password = "Sandopentorasus"

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{username}:{password}@localhost:5432/profiler_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "ai_dev_secret"