import sys
sys.path.append('.')

from app.models.product import Product
from app import create_app
from sqlalchemy import or_

app = create_app()
with app.app_context():
    # Simulate the chat API logic for "smart phonesbest battery high performance"
    query = Product.query
    
    # Build OR conditions just like the chat API
    category_conditions = []
    
    # Basic category parsing
    category_conditions.append(Product.category == 'smartphones')
    category_conditions.append(Product.subcategory == 'smartphones')
    
    # Performance-related conditions  
    user_query_lower = 'smart phonesbest battery high performance'
    if any(keyword in user_query_lower for keyword in ['phone', 'mobile', 'smartphone']):
        category_conditions.extend([
            Product.category == 'smartphones',
            Product.subcategory == 'smartphones'
        ])
        
        # For performance/flagship phones
        if any(keyword in user_query_lower for keyword in ['performance', 'best', 'flagship', 'powerful', 'fast']):
            category_conditions.extend([
                Product.style == 'premium',
                Product.style == 'gaming', 
                Product.subcategory == 'flagship'
            ])
    
    # Apply OR logic
    if category_conditions:
        query = query.filter(or_(*category_conditions))
    
    products = query.order_by(
        Product.rating.desc(),
        Product.stock_quantity.desc()
    ).limit(20).all()
    
    print(f"Found {len(products)} products:")
    for p in products:
        print(f"  - {p.name} (${p.price}) [{p.category}/{p.subcategory}] - {p.style}")
        if hasattr(p, 'features') and p.features:
            print(f"    Features: {p.features}")
