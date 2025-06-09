import requests
import json

# Test the mobile phone search with OR logic
def test_mobile_search():
    url = "http://localhost:5000/chat/message"
    
    # Login token (using test user)
    login_response = requests.post("http://localhost:5000/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    
    if login_response.status_code == 200:
        token = login_response.json()['access_token']
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Test query for mobile phones with casual/low pricing
        test_query = "mobile phone casual low pricing"
        
        response = requests.post(url, json={
            "message": test_query,
            "session_id": "test_mobile_search"
        }, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Query: {test_query}")
            print(f"Response: {data['message']}")
            print(f"Products found: {len(data.get('products', []))}")
            
            for product in data.get('products', []):
                print(f"  - {product['name']} (${product['price']}) [{product['category']}/{product['subcategory']}] - {product['style']}")
                
        else:
            print(f"Error: {response.status_code} - {response.text}")
    else:
        print(f"Login failed: {login_response.status_code}")

if __name__ == "__main__":
    test_mobile_search()
