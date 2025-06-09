#!/usr/bin/env python3
"""
Test script to verify the complete checkout flow:
1. Register/Login a user
2. Add items to cart
3. Create an order with complete checkout data
"""

import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:5000/api"

def test_checkout_flow():
    print("=== Testing Complete Checkout Flow ===\n")
    
    # Test user credentials
    test_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    session = requests.Session()
    
    # Step 1: Register or login user
    print("1. Registering/logging in user...")
    try:
        # Try to register
        register_response = session.post(f"{BASE_URL}/auth/register", json=test_user)
        if register_response.status_code == 201:
            print("✓ User registered successfully")
        elif register_response.status_code == 400:
            print("User already exists, logging in...")
    except Exception as e:
        print(f"Registration failed: {e}")
    
    # Login to get token
    login_response = session.post(f"{BASE_URL}/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return
    
    login_data = login_response.json()
    token = login_data.get("access_token")
    print("✓ Login successful")
    
    # Set authorization header
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Get products and add to cart
    print("\n2. Getting products and adding to cart...")
    
    # Get available products
    products_response = session.get(f"{BASE_URL}/products/", headers=headers)
    if products_response.status_code != 200:
        print(f"❌ Failed to get products: {products_response.text}")
        return
    
    products = products_response.json().get("products", [])
    if not products:
        print("❌ No products available")
        return
    
    print(f"✓ Found {len(products)} products")
    
    # Add first product to cart
    first_product = products[0]
    cart_item = {
        "product_id": first_product["id"],
        "quantity": 2
    }
    
    add_to_cart_response = session.post(f"{BASE_URL}/cart/items", json=cart_item, headers=headers)
    if add_to_cart_response.status_code != 201:
        print(f"❌ Failed to add to cart: {add_to_cart_response.text}")
        return
    
    print(f"✓ Added {first_product['name']} to cart")
    
    # Step 3: Get cart to verify
    print("\n3. Verifying cart contents...")
    cart_response = session.get(f"{BASE_URL}/cart/", headers=headers)
    if cart_response.status_code != 200:
        print(f"❌ Failed to get cart: {cart_response.text}")
        return
    
    cart_data = cart_response.json()
    cart_items = cart_data.get("cart", {}).get("items", [])
    print(f"✓ Cart has {len(cart_items)} items")
    
    # Step 4: Create order with complete checkout data
    print("\n4. Creating order with complete checkout data...")
    
    checkout_data = {
        "shipping_address": "John Doe, 123 Main St, Apt 4B, New York, NY 10001, United States",
        "billing_address": "John Doe, 456 Billing Ave, Suite 2A, New York, NY 10002, United States",
        "payment_method": "card",
        "customer_email": "john.doe@example.com",
        "customer_phone": "+1-555-0123",
        "payment_details": {
            "card_last_four": "1234",
            "card_type": "card",
            "cardholder_name": "John Doe"
        }
    }
    
    order_response = session.post(f"{BASE_URL}/orders/", json=checkout_data, headers=headers)
    if order_response.status_code != 201:
        print(f"❌ Failed to create order: {order_response.text}")
        return
    
    order_data = order_response.json()
    order_id = order_data.get("order", {}).get("id")
    print(f"✓ Order created successfully with ID: {order_id}")
    
    # Step 5: Verify order details
    print("\n5. Verifying order details...")
    order_detail_response = session.get(f"{BASE_URL}/orders/{order_id}", headers=headers)
    if order_detail_response.status_code != 200:
        print(f"❌ Failed to get order details: {order_detail_response.text}")
        return
    
    order_details = order_detail_response.json().get("order", {})
    print("✓ Order details retrieved:")
    print(f"  - Order ID: {order_details.get('id')}")
    print(f"  - Total Amount: ${order_details.get('total_amount')}")
    print(f"  - Status: {order_details.get('status')}")
    print(f"  - Payment Status: {order_details.get('payment_status')}")
    print(f"  - Customer Email: {order_details.get('customer_email')}")
    print(f"  - Customer Phone: {order_details.get('customer_phone')}")
    print(f"  - Shipping Address: {order_details.get('shipping_address')}")
    print(f"  - Billing Address: {order_details.get('billing_address')}")
    print(f"  - Items: {len(order_details.get('items', []))}")
    
    # Step 6: Verify cart is empty after order
    print("\n6. Verifying cart is empty after order...")
    cart_after_response = session.get(f"{BASE_URL}/cart/", headers=headers)
    if cart_after_response.status_code == 200:
        cart_after_data = cart_after_response.json()
        cart_after_items = cart_after_data.get("cart", {}).get("items", [])
        if len(cart_after_items) == 0:
            print("✓ Cart is empty after order creation")
        else:
            print(f"⚠️ Cart still has {len(cart_after_items)} items")
    
    print("\n=== Checkout Flow Test Completed Successfully! ===")

if __name__ == "__main__":
    test_checkout_flow()
