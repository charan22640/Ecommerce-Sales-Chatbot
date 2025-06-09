import requests
import os
from dotenv import load_dotenv
import logging
from typing import Dict, List, Any
import json
import re

# Load environment variables
load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("GEMINI_API_KEY not set in environment variables")
            self.api_url = None
            return
        
        # Use REST API endpoint that works
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
        
        # Test the API connection
        try:
            test_response = self._make_api_request("Hello, test connection")
            if test_response:
                print("✅ Successfully initialized Gemini service with REST API")
            else:
                print("❌ Failed to connect to Gemini API")
                self.api_url = None
        except Exception as e:
            print(f"❌ Error initializing Gemini service: {e}")
            self.api_url = None

        # Enhanced conversational system prompt
        self.system_prompt = """You are an expert electronics sales assistant with a friendly, helpful personality. Your name is Alex and you work at TechHub Electronics Store.

PERSONALITY TRAITS:
- Enthusiastic about technology
- Patient and understanding
- Ask clarifying questions when needed
- Provide personalized recommendations
- Explain technical concepts in simple terms
- Always helpful and positive

CONVERSATION GUIDELINES:
1. ALWAYS respond in a natural, conversational way
2. Show genuine interest in helping the customer
3. Ask follow-up questions to better understand their needs
4. Provide context for your recommendations
5. Mention specific product features that matter to their use case
6. Be empathetic to budget constraints
7. Offer alternatives when exact matches aren't available

PRODUCT EXPERTISE:
- Electronics and tech products ONLY
- Categories: computers, smartphones, audio, gaming, accessories
- Understand use cases: work, gaming, student, creative, casual
- Know about specifications, compatibility, and value propositions

RESPONSE STYLE:
- Start with acknowledgment of their request
- Ask clarifying questions when helpful
- Provide 2-3 specific recommendations with reasons
- Include key specifications and benefits
- End with an engaging question or offer to help further
- Use natural language, avoid robotic responses

IMPORTANT: If they ask about non-electronics (clothing, food, furniture), politely redirect to electronics while being helpful."""

        # Query parsing prompt (separate from conversation)
        self.parsing_prompt = """Extract product search criteria from user queries about electronics.

ELECTRONICS CATEGORIES:
- computers: laptops, desktops, tablets, monitors
- smartphones: phones, iphones, android
- audio: headphones, speakers, earbuds, airpods
- gaming: consoles, controllers, games
- accessories: chargers, cables, keyboards, mice

ATTRIBUTES:
- Colors: black, white, silver, space-gray, navy, rose-gold, red, blue
- Styles: premium, budget, gaming, professional, casual, student
- Storage: 128GB, 256GB, 512GB, 1TB, 2TB
- Price ranges from user budget mentions

Return JSON with extracted filters:
{
    "category": string,
    "subcategory": string,
    "style": string,
    "color": string,
    "storage": string,
    "price_range": {"min": number, "max": number}
}

If not electronics-related, return: {}"""

    def _make_api_request(self, prompt: str, max_retries: int = 3) -> str:
        """Make a request to the Gemini REST API."""
        if not self.api_url:
            return None

        headers = {
            'Content-Type': 'application/json'
        }

        body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=body,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if 'candidates' in data and len(data['candidates']) > 0:
                        return data['candidates'][0]['content']['parts'][0]['text']
                else:
                    print(f"API request failed with status {response.status_code}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Request error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    continue
                    
            except Exception as e:
                print(f"Unexpected error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    continue

        return None

    def extract_features(self, text: str) -> Dict:
        """Extract product features from user query."""
        if not self.api_url:
            return self._fallback_parse_query(text)
        
        prompt = self.parsing_prompt + f"\n\nUser query: {text}"
        
        try:
            response_text = self._make_api_request(prompt)
            if response_text:
                # Extract JSON from response
                match = re.search(r'\{[\s\S]*\}', response_text)
                if match:
                    features = json.loads(match.group())
                    return features
        except Exception as e:
            print(f"Error extracting features: {str(e)}")
        
        return self._fallback_parse_query(text)

    def get_product_recommendations(self, features: Dict, products: List[Dict], limit: int = 5) -> List[Dict]:
        """Get product recommendations based on extracted features."""
        if not features or not products:
            return []

        scored_products = []
        for product in products:
            score = 0
            
            # Category match
            if features.get('category') and features['category'].lower() == product['category'].lower():
                score += 3
            
            # Subcategory match
            if features.get('subcategory') and features['subcategory'].lower() == product['subcategory'].lower():
                score += 2
            
            # Style match
            if features.get('style') and features['style'].lower() == product['style'].lower():
                score += 2
            
            # Color match
            if features.get('color') and features['color'].lower() == product['color'].lower():
                score += 1
            
            # Storage match
            if features.get('storage') and features['storage'] == product.get('size'):
                score += 1
            
            # Price range match
            if features.get('price_range'):
                price = float(product['price'])
                if (not features['price_range']['min'] or price >= features['price_range']['min']) and \
                   (not features['price_range']['max'] or price <= features['price_range']['max']):
                    score += 2
            
            if score > 0:
                scored_products.append((score, product))
        
        # Sort by score and return top N products
        scored_products.sort(reverse=True, key=lambda x: x[0])
        return [product for _, product in scored_products[:limit]]

    def generate_response(self, query: str, products: List[Dict], conversation_history: List[Dict] = None) -> str:
        """Generate a natural, conversational response based on the query and matching products."""
        if not self.api_url:
            return "I apologize, but I'm unable to process your request right now. Please try again later!"

        try:
            # Prepare conversation context
            context = ""
            if conversation_history:
                recent_history = conversation_history[-4:]  # Last 4 messages for context
                context = "\n\nRECENT CONVERSATION:\n"
                for msg in recent_history:
                    role = "Customer" if not msg.get('is_bot') else "Alex"
                    context += f"{role}: {msg['message']}\n"

            # Prepare product information
            if products:
                product_info = "\n\nAVAILABLE PRODUCTS:\n"
                for i, product in enumerate(products[:5], 1):  # Top 5 products
                    product_info += f"{i}. {product['name']} - ${product['price']:.2f}\n"
                    product_info += f"   Category: {product['category']}, Style: {product.get('style', 'N/A')}\n"
                    product_info += f"   Rating: {product.get('rating', 0):.1f}/5, Stock: {product.get('stock_quantity', 0)}\n"
                    if product.get('description'):
                        product_info += f"   Description: {product['description'][:100]}...\n"
                    product_info += "\n"
            else:
                product_info = "\n\nNO MATCHING PRODUCTS FOUND in our electronics inventory."

            # Create conversational prompt
            conversation_prompt = f"""{self.system_prompt}

CURRENT SITUATION:
Customer Query: "{query}"
{context}
{product_info}

TASK: Respond as Alex, the friendly electronics sales assistant. Make your response natural and conversational:

1. If products are available:
   - Acknowledge their request warmly
   - Recommend 2-3 best products with specific reasons why they're good fits
   - Mention key features that matter for their use case
   - Include prices naturally in conversation
   - Ask a follow-up question to help them choose or learn more about their needs

2. If no products found:
   - Acknowledge what they're looking for
   - Explain why no matches were found (but stay positive)
   - Suggest similar alternatives or ask clarifying questions
   - Offer to help them find something else

3. If query is unclear:
   - Ask friendly clarifying questions
   - Suggest specific examples
   - Show enthusiasm to help

STYLE: Be conversational, helpful, and enthusiastic. Avoid robotic or template-like responses."""

            response_text = self._make_api_request(conversation_prompt)
            if response_text:
                return response_text.strip()
            else:
                return "I'm having a bit of trouble processing that right now, but I'm here to help! Could you tell me what kind of electronics you're looking for? I'd love to find the perfect product for you!"

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I'm having a bit of trouble processing that right now, but I'm here to help! Could you tell me what kind of electronics you're looking for? I'd love to find the perfect product for you!"

    def parse_query(self, user_message: str) -> Dict:
        """Parse user query and extract relevant product filters."""
        if not self.api_url:
            return self._fallback_parse_query(user_message)
            
        try:
            prompt = f"{self.parsing_prompt}\n\nUser query: {user_message}"
            response_text = self._make_api_request(prompt)
            
            if response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                
                if start >= 0 and end > start:
                    return json.loads(response_text[start:end])
            
            return self._fallback_parse_query(user_message)
                    
        except Exception as e:
            print(f"Error in parse_query: {str(e)}")
            return self._fallback_parse_query(user_message)

    def _fallback_parse_query(self, user_message: str) -> Dict:
        """Simple keyword-based fallback for when Gemini is unavailable."""
        filters = {}
        message = user_message.lower()
        
        # Use case mapping
        use_cases = {
            'professional': {
                'keywords': ['work', 'office', 'business', 'professional', 'productivity'],
                'categories': ['computers', 'accessories'],
                'style': 'professional'
            },
            'gaming': {
                'keywords': ['gaming', 'games', 'play', 'entertainment', 'stream'],
                'categories': ['gaming', 'computers'],
                'style': 'gaming'
            },
            'student': {
                'keywords': ['school', 'college', 'university', 'study', 'education'],
                'categories': ['computers', 'accessories'],
                'style': 'student'
            },
            'casual': {
                'keywords': ['home', 'personal', 'daily', 'regular', 'basic'],
                'categories': ['smartphones', 'audio'],
                'style': 'casual'
            }
        }
        
        # Check for use cases
        for use_case, data in use_cases.items():
            if any(keyword in message for keyword in data['keywords']):
                filters['style'] = data['style']
                if 'category' not in filters and data['categories']:
                    filters['category'] = data['categories'][0]
                break
        
        # Category detection with better keyword mapping
        categories = {
            'audio': ['headphone', 'headphones', 'speaker', 'earbud', 'earbuds', 'soundbar', 'microphone', 'airpods', 'earphones', 'headset'],
            'computers': ['laptop', 'desktop', 'tablet', 'monitor', 'pc', 'computer', 'macbook'],
            'smartphones': ['phone', 'iphone', 'android', 'mobile', 'smartphone'],
            'gaming': ['console', 'controller', 'game', 'gaming', 'ps5', 'xbox', 'nintendo', 'playstation'],
            'accessories': ['charger', 'cable', 'power bank', 'storage', 'keyboard', 'mouse', 'adapter']
        }
        
        # Check categories
        for category, keywords in categories.items():
            if any(keyword in message for keyword in keywords):
                filters['category'] = category
                break
        
        # Storage size detection
        storage_sizes = ['128GB', '256GB', '512GB', '1TB', '2TB']
        for size in storage_sizes:
            if size.lower() in message:
                filters['storage'] = size
                break
        
        # Colors
        colors = ['black', 'white', 'silver', 'space-gray', 'navy', 'rose-gold', 'red', 'blue']
        for color in colors:
            if color in message:
                filters['color'] = color
                break
        
        # Price range
        price_matches = re.findall(r'under\s*(\d+)|below\s*(\d+)|(\d+)\s*-\s*(\d+)', message)
        if price_matches:
            filters['price_range'] = {}
            if price_matches[0][0] or price_matches[0][1]:  # "under X" or "below X"
                max_price = int(price_matches[0][0] or price_matches[0][1])
                filters['price_range'] = {'min': None, 'max': max_price}
            elif price_matches[0][2] and price_matches[0][3]:  # "X - Y"
                min_price = int(price_matches[0][2])
                max_price = int(price_matches[0][3])
                filters['price_range'] = {'min': min_price, 'max': max_price}
        
        return filters

    def handle_conversation(self, user_message: str, conversation_history: List[Dict] = None) -> Dict:
        """Handle different types of conversations intelligently."""
        if not self.api_url:
            return self._fallback_conversation(user_message)

        try:
            # Analyze conversation intent
            intent_prompt = f"""{self.system_prompt}

CONVERSATION HISTORY:
{self._format_conversation_history(conversation_history) if conversation_history else "No previous conversation"}

CURRENT MESSAGE: "{user_message}"

TASK: Analyze this conversation and determine:
1. Intent: product_search, greeting, question, comparison, complaint, other
2. Urgency: high, medium, low
3. Sentiment: positive, neutral, negative
4. Needs_products: true/false
5. Follow_up_needed: true/false

Return JSON:
{{
    "intent": "string",
    "urgency": "string", 
    "sentiment": "string",
    "needs_products": boolean,
    "follow_up_needed": boolean,
    "response_type": "product_recommendation|general_help|clarification|greeting"
}}"""

            response_text = self._make_api_request(intent_prompt)
            
            if response_text:
                # Extract JSON
                match = re.search(r'\{[\s\S]*\}', response_text)
                if match:
                    analysis = json.loads(match.group())
                    return analysis
            
            return self._fallback_conversation(user_message)
            
        except Exception as e:
            print(f"Error in conversation analysis: {str(e)}")
            return self._fallback_conversation(user_message)

    def _format_conversation_history(self, history: List[Dict]) -> str:
        """Format conversation history for AI context."""
        if not history:
            return ""
        
        formatted = ""
        for msg in history[-6:]:  # Last 6 messages
            role = "Customer" if not msg.get('is_bot') else "Alex"
            formatted += f"{role}: {msg['message']}\n"
        return formatted

    def _fallback_conversation(self, user_message: str) -> Dict:
        """Fallback conversation analysis when AI is unavailable."""
        message_lower = user_message.lower()
        
        # Simple intent detection
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            intent = "greeting"
            response_type = "greeting"
        elif any(word in message_lower for word in ['?', 'how', 'what', 'why', 'when', 'where']):
            intent = "question"
            response_type = "general_help"
        elif any(word in message_lower for word in ['show', 'find', 'looking for', 'need', 'want', 'search']):
            intent = "product_search"
            response_type = "product_recommendation"
        else:
            intent = "other"
            response_type = "clarification"
        
        return {
            "intent": intent,
            "urgency": "medium",
            "sentiment": "neutral",
            "needs_products": intent == "product_search",
            "follow_up_needed": True,
            "response_type": response_type
        }
