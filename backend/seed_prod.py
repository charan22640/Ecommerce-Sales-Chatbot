import os
import sys
from dotenv import load_dotenv
from app import create_app
from app.models.user import db
from enhanced_seed_data import get_electronics_products

# Load environment variables
load_dotenv()

def seed_production():
    """Seed the production database with products."""
    try:
        # Create Flask app with production config
        app = create_app('production')
        
        with app.app_context():
            # Get products data
            products_data = get_electronics_products()
            
            # Add products to database
            print(f"Adding {len(products_data)} products to database...")
            for product_data in products_data:
                product = Product(**product_data)
                db.session.add(product)
            
            # Commit changes
            db.session.commit()
            print("Successfully added products to database!")
            
            # Verify products were added
            from app.models.product import Product
            count = Product.query.count()
            print(f"Total products in database: {count}")
            
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    seed_production()
