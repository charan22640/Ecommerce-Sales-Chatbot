#!/usr/bin/env python3
"""
Enhanced Electronics Store Database Seeder
Creates a comprehensive database with realistic electronics products
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.product import Product
from enhanced_seed_data import get_electronics_products, get_budget_electronics
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_sample_users():
    """Create sample users for testing."""
    print("Creating sample users...")
    users = [
        {
            'username': 'admin',
            'email': 'admin@techub.com',
            'password': 'admin123'
        },
        {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        },
        {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'password': 'password123'
        }
    ]
    
    created_users = []
    for user_data in users:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if not existing_user:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            
            db.session.add(user)
            created_users.append(user)
            print(f"✅ Created user: {user.username}")
        else:
            print(f"⚠️  User {user_data['username']} already exists")
    
    return created_users

def create_products():
    """Create comprehensive product catalog."""
    print("🛍️  Creating comprehensive electronics catalog...")
    
    # Get all products
    all_products = get_electronics_products() + get_budget_electronics()
    
    created_products = []
    
    for product_data in all_products:
        # Check if product already exists
        existing_product = Product.query.filter_by(name=product_data['name']).first()
        if not existing_product:
            product = Product(**product_data)
            db.session.add(product)
            created_products.append(product)
            print(f"✅ Created product: {product.name} - ${product.price}")
        else:
            print(f"⚠️  Product {product_data['name']} already exists")
    
    return created_products

def main():
    """Main seeding function."""
    print("🚀 Starting Enhanced Electronics Store Database Seeding...")
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            logger.info("Creating database tables...")
            db.create_all()
            
            logger.info("Creating sample users...")
            users = create_sample_users()
            
            logger.info("Creating products...")
            products = create_products()
            
            # Commit all changes
            try:
                logger.info("Committing changes to database...")
                db.session.commit()
                print(f"\n🎉 Database seeding completed successfully!")
                print(f"📊 Created {len(users)} users")
                print(f"🛍️  Created {len(products)} products")
                print("\n📋 Summary of products by category:")
                
                # Show summary
                categories = {}
                for product in products:
                    category = product.category
                    if category not in categories:
                        categories[category] = 0
                    categories[category] += 1
                
                for category, count in categories.items():
                    print(f"   {category}: {count} products")
                    
                print(f"\n🔐 Sample login credentials:")
                print(f"   Admin: admin@techub.com / admin123")
                print(f"   User: test@example.com / password123")
                print(f"\n✅ Database is ready for use!")
                
            except Exception as e:
                logger.error(f"Error committing to database: {e}")
                db.session.rollback()
                return False
        
        except Exception as e:
            logger.error(f"Error during database seeding: {e}")
            return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
