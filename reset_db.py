from models.database import db
from app import create_app

def reset_database():
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database has been reset successfully!")

if __name__ == "__main__":
    reset_database()
