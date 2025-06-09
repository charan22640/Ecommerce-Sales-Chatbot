from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import db, User
from ..models.cart import Cart, CartItem
from ..models.order import Order, OrderItem
from ..models.product import Product

order_bp = Blueprint('order', __name__)

def handle_cors():
    """Handle CORS preflight requests"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    return None

@order_bp.before_request
def before_request():
    cors_response = handle_cors()
    if cors_response:
        return cors_response

@order_bp.route('/', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_orders():
    """Get user's order history"""
    if request.method == 'OPTIONS':
        return handle_cors()
    
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'orders': [order.to_dict() for order in orders]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_bp.route('/', methods=['POST', 'OPTIONS'])
@jwt_required()
def create_order():
    """Create order from cart"""
    if request.method == 'OPTIONS':
        return handle_cors()
    
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'shipping_address' not in data:
            return jsonify({'error': 'Shipping address is required'}), 400
        
        shipping_address = data['shipping_address']
        billing_address = data.get('billing_address', shipping_address)
        payment_method = data.get('payment_method', 'card')
        customer_email = data.get('customer_email', '')
        customer_phone = data.get('customer_phone', '')
        
        # Get user's cart
        user = User.query.get(user_id)
        if not user or not user.cart or not user.cart.items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        cart = user.cart
        total_amount = 0
        
        # Calculate total amount
        for cart_item in cart.items:
            if cart_item.product:
                total_amount += cart_item.product.price * cart_item.quantity
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=shipping_address,
            billing_address=billing_address,
            payment_method=payment_method,
            customer_email=customer_email,
            customer_phone=customer_phone,
            status='pending',
            payment_status='pending'
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
          # Create order items from cart items and update product stock
        for cart_item in cart.items:
            if cart_item.product:
                # Check if there's enough stock
                if cart_item.product.stock_quantity < cart_item.quantity:
                    db.session.rollback()
                    return jsonify({
                        'error': f'Insufficient stock for {cart_item.product.name}. Only {cart_item.product.stock_quantity} available.'
                    }), 400
                
                # Create order item
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                db.session.add(order_item)
                
                # Update product stock quantity
                cart_item.product.stock_quantity -= cart_item.quantity
        
        # Clear cart
        CartItem.query.filter_by(cart_id=cart.id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<int:order_id>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_order(order_id):
    """Get specific order details"""
    if request.method == 'OPTIONS':
        return handle_cors()
    
    try:
        user_id = get_jwt_identity()
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({
            'success': True,
            'order': order.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<int:order_id>/status', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_order_status(order_id):
    """Update order status (for admin or system use)"""
    if request.method == 'OPTIONS':
        return handle_cors()
    
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        new_status = data['status']
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        
        if new_status not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Only allow certain status changes by regular users
        if new_status == 'cancelled' and order.status in ['pending', 'confirmed']:
            order.status = new_status
        else:
            return jsonify({'error': 'Cannot update order status'}), 403
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order status updated',
            'order': order.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<int:order_id>/payment', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_payment_status(order_id):
    """Update payment status"""
    if request.method == 'OPTIONS':
        return handle_cors()
    
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'payment_status' not in data:
            return jsonify({'error': 'Payment status is required'}), 400
        
        payment_status = data['payment_status']
        valid_statuses = ['pending', 'completed', 'failed']
        
        if payment_status not in valid_statuses:
            return jsonify({'error': f'Invalid payment status. Must be one of: {valid_statuses}'}), 400
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order.payment_status = payment_status
        
        # If payment completed, update order status
        if payment_status == 'completed' and order.status == 'pending':
            order.status = 'confirmed'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Payment status updated',
            'order': order.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
