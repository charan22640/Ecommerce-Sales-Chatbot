#!/usr/bin/env python3
"""
Script to check and verify products in the database
"""
import os
import sys
import logging
from app import create_app, db
from app.models.product import Product

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_products():
    """Check products in the database"""
    try:
        # Create Flask app with production config
        app = create_app('production')
        
        with app.app_context():
            # Get all products
            products = Product.query.all()
            
            if not products:
                logger.warning("❌ No products found in the database!")
                return False
                
            logger.info(f"✅ Found {len(products)} products")
            
            # Show summary by category
            categories = {}
            for product in products:
                category = product.category
                if category not in categories:
                    categories[category] = []
                categories[category].append(product)
            
            logger.info("\n📊 Products by category:")
            for category, products in categories.items():
                logger.info(f"   {category}: {len(products)} products")
                # Show first 3 products in each category
                for product in products[:3]:
                    logger.info(f"      - {product.name} (${product.price})")
            
            return True
                    
    except Exception as e:
        logger.error(f"Error checking products: {e}")
        return False

if __name__ == "__main__":
    success = check_products()
    sys.exit(0 if success else 1)
