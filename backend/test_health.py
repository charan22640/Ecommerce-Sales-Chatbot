#!/usr/bin/env python3
"""
Simple health check script to test if the app starts correctly
"""

import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app():
    try:
        print("Testing app creation...")
        
        # Set required environment variables if not set
        if not os.getenv('SECRET_KEY'):
            os.environ['SECRET_KEY'] = 'test-secret-key'
        if not os.getenv('JWT_SECRET_KEY'):
            os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret'
        if not os.getenv('DATABASE_URL'):
            os.environ['DATABASE_URL'] = 'sqlite:///test.db'
        if not os.getenv('FLASK_ENV'):
            os.environ['FLASK_ENV'] = 'production'
        
        # Import and create app
        from app import create_app
        from config import config
        
        env = os.getenv('FLASK_ENV', 'production')
        app = create_app(env)
        
        print(f"✅ App created successfully with config: {env}")
        print(f"Debug mode: {app.debug}")
        print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
        
        # Test a simple route
        with app.test_client() as client:
            response = client.get('/')
            print(f"Health check response: {response.status_code}")
            print(f"Response data: {response.get_json()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_app()
    sys.exit(0 if success else 1)
