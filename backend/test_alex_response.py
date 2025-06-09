import sys
sys.path.append('.')

from app.services.gemini_service import GeminiService
from app.models.product import Product
from app import create_app
from sqlalchemy import or_

app = create_app()
with app.app_context():
    gemini = GeminiService()
    
    # Simulate the exact products that would be found
    query = Product.query
    category_conditions = [
        Product.category == 'smartphones',
        Product.style == 'premium',
        Product.style == 'gaming',
        Product.subcategory == 'flagship'
    ]
    
    query = query.filter(or_(*category_conditions))
    products = query.order_by(
        Product.rating.desc(),
        Product.stock_quantity.desc()
    ).limit(8).all()
    
    product_list = [product.to_dict() for product in products]
    
    print("Products that will be sent to Gemini:")
    for p in product_list:
        print(f"  - {p['name']} (${p['price']}) [{p['category']}/{p['subcategory']}]")
    
    # Generate response just like the chat API does
    user_message = "smart phonesbest battery high performance"
    response = gemini.generate_response(user_message, product_list, [])
    
    print(f"\nAlex's Response:")
    print(response)
