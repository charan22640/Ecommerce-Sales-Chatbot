from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    return jsonify({"message": "Cart endpoint working"}), 200

@cart_bp.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    return jsonify({"message": "Add to cart endpoint working"}), 200
