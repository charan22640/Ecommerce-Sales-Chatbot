import os
import sys
from dotenv import load_dotenv
import psycopg2
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def check_production_database():
    """Check the contents of the production database and seed if empty."""
    try:
        # Get the production DATABASE_URL from environment
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            logger.error("No DATABASE_URL found in environment variables")
            return

        # Connect to the database
        logger.info("Connecting to production database...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        # Check products table
        logger.info("Checking products table...")
        cur.execute("SELECT COUNT(*) FROM products")
        product_count = cur.fetchone()[0]
        logger.info(f"Total products in database: {product_count}")

        if product_count == 0:
            logger.warning("No products found in the database!")
        else:
            # Get sample of products
            logger.info("Fetching sample products...")
            cur.execute("""
                SELECT id, name, price, category, description 
                FROM products 
                LIMIT 5
            """)
            sample_products = cur.fetchall()
            logger.info("Sample products:")
            for product in sample_products:
                logger.info(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]}, Category: {product[3]}")

        # Check categories
        logger.info("\nChecking product categories...")
        cur.execute("""
            SELECT DISTINCT category, COUNT(*) 
            FROM products 
            GROUP BY category
        """)
        categories = cur.fetchall()
        logger.info("Products by category:")
        for category in categories:
            logger.info(f"{category[0]}: {category[1]} products")

    except Exception as e:
        logger.error(f"Error checking production database: {str(e)}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_production_database()
