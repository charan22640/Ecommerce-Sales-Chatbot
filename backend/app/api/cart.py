from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from ..models.user import db, User
from ..models.cart import Cart, CartItem
from ..models.product import Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET', 'OPTIONS'])
def get_cart():
    """Get current user's cart"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
    
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get or create cart
        cart = user.cart
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'cart': cart.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/items', methods=['POST', 'OPTIONS'])
def add_to_cart():
    """Add item to cart"""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
    
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        data = request.get_json()
        if not data or 'product_id' not in data:
            return jsonify({'error': 'Product ID is required'}), 400
        
        product_id = data['product_id']
        quantity = data.get('quantity', 1)
        
        # Validate product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get or create cart
        user = User.query.get(user_id)
        cart = user.cart
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
        
        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        
        if existing_item:
            existing_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item added to cart',
            'cart': cart.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
