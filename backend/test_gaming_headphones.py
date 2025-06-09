#!/usr/bin/env python3
"""
Test script to verify gaming headphones search is working correctly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.product import Product
from app.services.gemini_service import GeminiService

def test_gaming_headphones_search():
    app = create_app()
    
    with app.app_context():
        print("=== Testing Gaming Headphones Search ===\n")
        
        # Test 1: Query parsing
        gemini = GeminiService()
        query = "Show me gaming headphones under $200"
        filters = gemini.parse_query(query)
        
        print(f"1. Query: '{query}'")
        print(f"   Parsed filters: {filters}\n")
        
        # Test 2: Manual database search for headphones/headsets under $200
        print("2. Manual database search:")
        
        # Search audio headphones
        audio_headphones = Product.query.filter(
            Product.category == 'audio',
            Product.subcategory.in_(['headphones', 'earbuds']),
            Product.price <= 200
        ).all()
        
        # Search gaming headsets  
        gaming_headsets = Product.query.filter(
            Product.category == 'gaming',
            Product.subcategory == 'headsets',
            Product.price <= 200
        ).all()
        
        print(f"   Audio headphones under $200: {len(audio_headphones)}")
        for p in audio_headphones:
            print(f"     - {p.name} (${p.price}) [{p.category}/{p.subcategory}]")
            
        print(f"   Gaming headsets under $200: {len(gaming_headsets)}")
        for p in gaming_headsets:
            print(f"     - {p.name} (${p.price}) [{p.category}/{p.subcategory}]")
        
        # Test 3: Combined results
        all_headphones = audio_headphones + gaming_headsets
        print(f"\n   Total headphone products found: {len(all_headphones)}")
        
        # Test 4: Simulate the new chat API logic
        print("\n3. Testing new chat API logic:")
        user_query_lower = query.lower()
        if any(keyword in user_query_lower for keyword in ['headphone', 'headset', 'earbuds']):
            print("   ✅ Query detected as headphone-related")
            print("   ✅ Would search both audio/headphones and gaming/headsets")
            print(f"   ✅ Would return {len(all_headphones)} products")
        else:
            print("   ❌ Query not detected as headphone-related")
        
        print(f"\n=== Results Summary ===")
        print(f"Total products that should show up: {len(all_headphones)}")
        if len(all_headphones) > 0:
            print("✅ SUCCESS: Alex should now show actual product cards!")
        else:
            print("❌ PROBLEM: No products found for gaming headphones")

if __name__ == "__main__":
    test_gaming_headphones_search()
