#!/usr/bin/env python3
"""
Deployment validation script for Render
Run this before deploying to check for common issues
"""

import os
import sys
import importlib.util

def check_dependencies():
    """Check if all required dependencies are importable"""
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'flask_migrate',
        'flask_jwt_extended',
        'flask_cors',
        'gunicorn',
        'psycopg2',
        'redis'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"✗ {package}")
    
    return missing

def check_environment():
    """Check required environment variables"""
    required_env = [
        'FLASK_ENV',
        'SECRET_KEY', 
        'JWT_SECRET_KEY',
        'DATABASE_URL'
    ]
    
    missing = []
    for var in required_env:
        if os.getenv(var):
            print(f"✓ {var}")
        else:
            missing.append(var)
            print(f"✗ {var}")
    
    return missing

def check_config():
    """Check if config can be imported"""
    try:
        import config
        print("✓ Config module imports successfully")
        
        # Test configuration objects
        prod_config = config.ProductionConfig()
        print("✓ ProductionConfig instantiates successfully")
        return True
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False

def check_app():
    """Check if app can be created"""
    try:
        from app import create_app
        app = create_app('production')
        print("✓ App creates successfully")
        return True
    except Exception as e:
        print(f"✗ App creation error: {e}")
        return False

def main():
    print("=== Render Deployment Check ===\n")
    
    print("1. Checking dependencies...")
    missing_deps = check_dependencies()
    
    print("\n2. Checking environment variables...")
    missing_env = check_environment()
    
    print("\n3. Checking configuration...")
    config_ok = check_config()
    
    print("\n4. Checking app creation...")
    app_ok = check_app()
    
    print("\n=== Summary ===")
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
    if missing_env:
        print(f"Missing environment variables: {', '.join(missing_env)}")
    if not config_ok:
        print("Configuration issues detected")
    if not app_ok:
        print("App creation issues detected")
    
    if not missing_deps and not missing_env and config_ok and app_ok:
        print("✅ All checks passed! Ready for deployment.")
        return 0
    else:
        print("❌ Issues detected. Please fix before deploying.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
