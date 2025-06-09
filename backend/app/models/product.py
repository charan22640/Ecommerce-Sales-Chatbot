from datetime import datetime
from .user import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., 'tops', 'bottoms', 'dresses'
    subcategory = db.Column(db.String(50))  # e.g., 't-shirts', 'jeans', 'maxi-dresses'
    style = db.Column(db.String(50))  # e.g., 'casual', 'formal', 'party'
    color = db.Column(db.String(50))
    size = db.Column(db.String(20))
    rating = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(500))  
    stock_quantity = db.Column(db.Integer, default=0)
    specifications = db.Column(db.Text)  # JSON string for product specifications
    features = db.Column(db.Text)        # JSON string for special features like "high bass", "high volume"
    brand = db.Column(db.String(100))    # Product brand
    model = db.Column(db.String(100))    # Product model
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, description, price, category, **kwargs):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        for key, value in kwargs.items():
            setattr(self, key, value)
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'subcategory': self.subcategory,
            'style': self.style,
            'color': self.color,
            'size': self.size,
            'rating': self.rating,
            'image_url': self.image_url,
            'stock_quantity': self.stock_quantity,
            'brand': self.brand,
            'model': self.model,
            'specifications': json.loads(self.specifications) if self.specifications else {},
            'features': json.loads(self.features) if self.features else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Product {self.name}>' 