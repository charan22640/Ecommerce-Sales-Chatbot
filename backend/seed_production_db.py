import os
import sys
import psycopg2
from psycopg2.extras import execute_values
import logging
from enhanced_seed_data import get_electronics_products, get_budget_electronics

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_production_database():
    """Seed the production database with products."""
    try:
        # Use the Render production database URL
        database_url = 'postgres://ecommerce_db_user:MnuGPLxdjxhG5AbMTXRR2Td8l2wIvPR3@dpg-cjkj8ht37rbc738v5q50-a.oregon-postgres.render.com/ecommerce_db'
        
        logger.info("Connecting to production database...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        # Check if products exist
        cur.execute("SELECT COUNT(*) FROM products")
        product_count = cur.fetchone()[0]
        logger.info(f"Found {product_count} existing products")

        if product_count == 0:
            # Get products data
            all_products = get_electronics_products() + get_budget_electronics()
            
            # Prepare products for insertion
            products_data = [(
                p['name'],
                p['description'],
                p['price'],
                p['category'],
                p.get('subcategory', ''),
                p.get('brand', ''),
                p.get('image_url', ''),
                p.get('stock', 100),
                True  # is_active
            ) for p in all_products]

            # Insert products
            logger.info(f"Inserting {len(products_data)} products...")
            insert_query = """
                INSERT INTO products 
                (name, description, price, category, subcategory, brand, image_url, stock, is_active)
                VALUES %s
            """
            execute_values(cur, insert_query, products_data)
            
            # Commit the transaction
            conn.commit()
            logger.info("✅ Products inserted successfully!")

            # Verify insertion
            cur.execute("SELECT COUNT(*) FROM products")
            new_count = cur.fetchone()[0]
            logger.info(f"Total products after seeding: {new_count}")

        else:
            logger.info("Products already exist in database, no seeding needed")

        # Show category summary
        cur.execute("""
            SELECT category, COUNT(*) 
            FROM products 
            GROUP BY category
        """)
        categories = cur.fetchall()
        logger.info("\n📊 Products by category:")
        for category, count in categories:
            logger.info(f"   {category}: {count} products")

    except Exception as e:
        logger.error(f"Error seeding production database: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    seed_production_database()
