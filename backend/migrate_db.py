"""
Database Migration Script - Add Stories Table
Run this once to create the stories table
"""

from app import app, db
from models import User, Story

def create_tables():
    with app.app_context():
        print("🔄 Creating database tables...")
        
        # Create all tables
        db.create_all()
        
        print("✅ Database tables created successfully!")
        print("   - users table")
        print("   - stories table")
        
        # Verify tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\n📋 Current tables: {tables}")

if __name__ == '__main__':
    create_tables()
