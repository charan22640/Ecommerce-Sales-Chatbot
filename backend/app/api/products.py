from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os
from ..models.product import Product
from ..models.user import db
from sqlalchemy import or_
# Image handling removed as we're using direct URLs

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    # Get query parameters
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    style = request.args.get('style')
    color = request.args.get('color')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search')
    
    # Start with base query
    query = Product.query
    
    # Apply filters
    if category:
        query = query.filter(Product.category == category)
    if subcategory:
        query = query.filter(Product.subcategory == subcategory)
    if style:
        query = query.filter(Product.style == style)
    if color:
        query = query.filter(Product.color == color)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    # Apply search if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Execute query with pagination
    pagination = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'products': [product.to_dict() for product in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = request.get_json()
        
        new_product = Product(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            category=data.get('category'),
            subcategory=data.get('subcategory'),
            style=data.get('style'),
            color=data.get('color'),
            size=data.get('size'),
            rating=data.get('rating', 0.0),
            image_url=data.get('image_url', ''),
            stock_quantity=data.get('stock_quantity', 0)
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({'message': 'Product created successfully', 'product': new_product.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    # Update product fields
    for field, value in data.items():
        if hasattr(product, field):
            setattr(product, field, value)
    
    db.session.commit()
    
    return jsonify(product.to_dict())

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted successfully'})

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Product.category).distinct().all()
    return jsonify([category[0] for category in categories])

@products_bp.route('/subcategories', methods=['GET'])
def get_subcategories():
    subcategories = db.session.query(Product.subcategory).distinct().all()
    return jsonify([subcategory[0] for subcategory in subcategories if subcategory[0]])

@products_bp.route('/uploads/<path:filename>')
def serve_image(filename):
    """Serve uploaded images."""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)