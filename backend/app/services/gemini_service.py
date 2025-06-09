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
            self.api_url = None        # Enhanced conversational system prompt
        self.system_prompt = """You are Alex, the premium AI shopping assistant at NexTechAI - the leading destination for cutting-edge electronics and smart technology solutions. You represent NexTechAI's commitment to innovation, quality, and exceptional customer experience.

COMPANY IDENTITY - NexTechAI:
🚀 NexTechAI - Next Generation Technology & AI Solutions
- Premium electronics and smart technology marketplace
- Curated collection of latest smartphones, high-performance laptops, immersive gaming gear, premium audio equipment
- AI-powered personalized shopping experience with intelligent recommendations
- Committed to bringing customers the most innovative and reliable tech products
- Expert guidance for finding perfect technology solutions for every need

BRAND VOICE & PERSONALITY:
- Professional yet approachable and enthusiastic about technology
- Knowledgeable expert who understands customer needs
- Confident in NexTechAI's premium product quality and selection
- Helpful guide who makes technology accessible and exciting
- Always mention NexTechAI when discussing product recommendations

CORE BEHAVIOR:
- Be conversational but professional (2-3 sentences max per section)
- IMMEDIATELY showcase NexTechAI's premium product offerings when matches are found
- Emphasize NexTechAI's curated selection and AI-powered recommendations
- Focus on specific product benefits and why they're perfect for customer needs
- Be enthusiastic about NexTechAI's innovative technology solutions

RESPONSE STRATEGY:
1. Warm greeting acknowledging customer's needs and NexTechAI's expertise
2. IMMEDIATELY present 2-3 best product recommendations from NexTechAI's collection
3. For each product: highlight name, price, and ONE compelling benefit/feature
4. End with simple question about preferences or offer more help

CONVERSATION STYLE:
- Keep responses short and actionable
- Highlight NextechAI's expertise in premium technology
- Show products first, ask questions second
- Highlight specific features that matter (gaming performance, battery life, sound quality)
- Mention prices naturally
- Be helpful but direct
- ALWAYS focus on what IS available, never mention what ISN'T available
- If exact match isn't found, show closest alternatives without negative statements

EXAMPLE GOOD RESPONSE:
"Great choice looking for headphones! Here are my top picks:

🎧 Sony WH-1000XM5 ($399) - Amazing noise cancellation, perfect for travel
🎧 JBL Charge 5 ($179) - Incredible bass and waterproof for outdoor use  
🎧 Bose QuietComfort ($329) - Supreme comfort for long listening sessions

Which type of listening do you do most - travel, exercise, or at home?"

CRITICAL RULES:
- NEVER say "I don't have", "we don't have", "not available", "unfortunately"
- ALWAYS show what you DO have instead
- Focus on benefits and positive aspects
- If no perfect match, show closest alternatives as great options

AVOID:
- Long explanatory paragraphs
- Multiple clarifying questions before showing products
- Technical jargon without context
- Being overly chatty
- Negative statements about availability

Remember: Show products fast, be helpful, stay concise!

IMPORTANT: If they ask about non-electronics (clothing, food, furniture), politely redirect to electronics while being helpful."""        # Query parsing prompt (separate from conversation)
        self.parsing_prompt = """Extract product search criteria from user queries about NexTechAI's premium electronics collection.

NEXTECHAI ELECTRONICS CATEGORIES:
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
                return "Hi there! I'm Alex from NexTechAI, and I'm here to help you discover amazing technology solutions! 🚀 Could you tell me what kind of premium electronics you're looking for? Whether it's laptops, smartphones, gaming gear, or audio equipment - I'll find the perfect NexTechAI products for you!"

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "Hi there! I'm Alex from NexTechAI, and I'm here to help you discover amazing technology solutions! 🚀 Could you tell me what kind of premium electronics you're looking for? Whether it's laptops, smartphones, gaming gear, or audio equipment - I'll find the perfect NexTechAI products for you!"

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

    def generate_suggestions(self, query: str, products: List[Dict], conversation_type: str) -> List[str]:
        """Generate smart follow-up suggestions based on the current context."""
        try:
            suggestions_prompt = f"""
As Alex, an electronics shopping assistant, generate 6 helpful follow-up questions/suggestions based on this conversation context:

Customer Query: "{query}"
Conversation Type: {conversation_type}
Products Found: {len(products) if products else 0}

Product Categories: {list(set([p.get('category', '') for p in products])) if products else []}

Generate suggestions that would naturally follow this conversation. Make them:
1. Contextually relevant
2. Action-oriented
3. Helpful for decision making
4. Varied in scope (specific product questions, comparisons, alternatives, etc.)

Return ONLY 6 suggestions, one per line, without numbering or bullets.
Examples of good suggestions:
- "Tell me more about the first product"
- "Which has the best battery life?"
- "Show me budget alternatives under $200"
- "Any wireless options available?"
- "What's the difference between these models?"
- "Which would you recommend for a student?"
"""

            if not self.api_url:
                # Fallback suggestions
                return self._fallback_suggestions(conversation_type, products)
            
            response_text = self._make_api_request(suggestions_prompt)
            if response_text:
                suggestions = [s.strip() for s in response_text.strip().split('\n') if s.strip()]
                return suggestions[:6]  # Limit to 6 suggestions
            else:
                return self._fallback_suggestions(conversation_type, products)

        except Exception as e:
            print(f"Error generating suggestions: {str(e)}")
            return self._fallback_suggestions(conversation_type, products)

    def _fallback_suggestions(self, conversation_type: str, products: List[Dict]) -> List[str]:
        """Fallback suggestions when API is not available."""
        base_suggestions = [
            "Show me more options",
            "What's your best recommendation?",
            "Any budget alternatives?",
            "Tell me about the warranties",
            "Show me customer reviews",
            "Compare top 3 products"
        ]
        
        if conversation_type == 'product_recommendation' and products:
            if any('smartphone' in str(p.get('category', '')).lower() for p in products):
                return [
                    "Which has the best camera?",
                    "Show me phones with long battery life",
                    "Any 5G compatible models?",
                    "What about storage options?",
                    "Which is best for gaming?",
                    "Show me budget alternatives"
                ]
            elif any('audio' in str(p.get('category', '')).lower() for p in products):
                return [
                    "Which has the best sound quality?",
                    "Any noise-canceling options?",
                    "Show me wireless models",
                    "What about battery life?",
                    "Which is most comfortable?",
                    "Any budget alternatives?"
                ]
            elif any('laptop' in str(p.get('category', '')).lower() for p in products):
                return [
                    "Which is best for gaming?",
                    "Show me lightweight options",
                    "Any 2-in-1 convertibles?",
                    "What about battery life?",
                    "Which has the best display?",
                    "Show me budget alternatives"
                ]
        
        return base_suggestions
