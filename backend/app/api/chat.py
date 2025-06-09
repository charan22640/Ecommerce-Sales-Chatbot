from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, and_
from ..models.chat import ChatMessage
from ..models.product import Product
from ..models.user import db
from ..services.gemini_service import GeminiService
import uuid

chat_bp = Blueprint('chat', __name__)
gemini_service = GeminiService()

@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get or create session ID
        session_id = data.get('session_id') or str(uuid.uuid4())
        
        # Store user message
        user_message = ChatMessage(
            user_id=current_user_id,
            message=data['message'],
            is_bot=False,
            session_id=session_id,
            message_metadata={}
        )
        db.session.add(user_message)
        db.session.commit()
        
        try:
            # Get conversation history for context
            conversation_history = ChatMessage.query.filter_by(
                user_id=current_user_id,
                session_id=session_id
            ).order_by(ChatMessage.created_at.desc()).limit(10).all()
            
            history_list = [msg.to_dict() for msg in reversed(conversation_history)]
            
            # Analyze conversation intent
            conversation_analysis = gemini_service.handle_conversation(
                data['message'], 
                history_list
            )
              # Handle different conversation types
            if conversation_analysis.get('intent') == 'greeting':
                response_msg = gemini_service.generate_response(
                    data['message'], 
                    [], 
                    history_list
                )
                
                # Generate welcome suggestions
                suggestions = [
                    "I need a laptop for work",
                    "Show me gaming headphones",
                    "Looking for a smartphone",
                    "Best tablets for students",
                    "Wireless earbuds under $100",
                    "What's trending in electronics?"
                ]
                
                bot_message = ChatMessage(
                    user_id=current_user_id,
                    message=response_msg,
                    is_bot=True,
                    session_id=session_id,
                    message_metadata={
                        'conversation_analysis': conversation_analysis,
                        'suggestions': suggestions
                    }
                )
                db.session.add(bot_message)
                db.session.commit()
                
                return jsonify({
                    'message': response_msg,
                    'session_id': session_id,
                    'products': [],
                    'conversation_type': 'greeting',
                    'suggestions': suggestions
                })
            
            elif conversation_analysis.get('needs_products', True):
                # Parse query for product search
                filters = gemini_service.parse_query(data['message'])                # Check if user is looking for non-electronics items
                if not filters:
                    non_electronics_keywords = [
                        'jeans', 'clothes', 'clothing', 'shoes', 'shirt', 'dress', 'pants', 
                        'jacket', 'furniture', 'food', 'books', 'medicine', 'grocery'
                    ]
                    user_query_lower = data['message'].lower()
                    
                    if any(keyword in user_query_lower for keyword in non_electronics_keywords):
                        response_msg = gemini_service.generate_response(
                            f"Customer asked about non-electronics: {data['message']}", 
                            [], 
                            history_list
                        )
                    else:
                        response_msg = gemini_service.generate_response(
                            data['message'], 
                            [], 
                            history_list
                        )
                    
                    # Generate clarification suggestions
                    suggestions = [
                        "Show me laptops instead",
                        "I need smartphones", 
                        "Looking for headphones",
                        "Show me tablets",
                        "Any gaming accessories?",
                        "What electronics do you have?"
                    ]
                    
                    bot_message = ChatMessage(
                        user_id=current_user_id,
                        message=response_msg,
                        is_bot=True,
                        session_id=session_id,
                        message_metadata={
                            'conversation_analysis': conversation_analysis,
                            'suggestions': suggestions
                        }
                    )
                    db.session.add(bot_message)
                    db.session.commit()
                    
                    return jsonify({
                        'message': response_msg,
                        'session_id': session_id,
                        'products': [],
                        'conversation_type': 'clarification',
                        'suggestions': suggestions
                    })
                  # Build product query with enhanced filters
                query = Product.query
                
                # Handle special cases for broader matching
                user_query_lower = data['message'].lower()
                
                # Special handling for headphones/headsets queries
                if any(keyword in user_query_lower for keyword in ['headphone', 'headset', 'earbuds']):
                    # Search in both audio and gaming categories for headphone-related products
                    audio_headphones = []
                    gaming_headsets = []
                    
                    # Get audio headphones/earbuds
                    audio_query = Product.query.filter(
                        Product.category == 'audio',
                        Product.subcategory.in_(['headphones', 'earbuds'])
                    )
                    
                    # Get gaming headsets
                    gaming_query = Product.query.filter(
                        Product.category == 'gaming',
                        Product.subcategory == 'headsets'
                    )
                    
                    # Apply price filter to both queries
                    if filters.get('price_range'):
                        if filters['price_range'].get('min'):
                            audio_query = audio_query.filter(Product.price >= filters['price_range']['min'])
                            gaming_query = gaming_query.filter(Product.price >= filters['price_range']['min'])
                        if filters['price_range'].get('max'):
                            audio_query = audio_query.filter(Product.price <= filters['price_range']['max'])
                            gaming_query = gaming_query.filter(Product.price <= filters['price_range']['max'])
                    
                    # Apply other filters
                    if filters.get('color'):
                        audio_query = audio_query.filter(Product.color == filters['color'])
                        gaming_query = gaming_query.filter(Product.color == filters['color'])
                    if filters.get('storage'):
                        audio_query = audio_query.filter(Product.size == filters['storage'])
                        gaming_query = gaming_query.filter(Product.size == filters['storage'])
                    
                    # Combine results
                    audio_products = audio_query.all()
                    gaming_products = gaming_query.all()
                    
                    # Merge and deduplicate
                    all_products = audio_products + gaming_products
                    seen_ids = set()
                    products = []
                    for p in all_products:
                        if p.id not in seen_ids:
                            products.append(p)
                            seen_ids.add(p.id)
                      # Sort by rating and stock
                    products.sort(key=lambda x: (-x.rating, -x.stock_quantity))
                    products = products[:20]
                
                else:
                    # Use OR logic for broader, more inclusive product matching
                    # This will show more products instead of being overly restrictive
                    
                    # Build OR conditions for broader category matching
                    category_conditions = []
                    
                    # Add the parsed category/subcategory
                    if filters.get('category'):
                        category_conditions.append(Product.category == filters['category'])
                    if filters.get('subcategory'):
                        category_conditions.append(Product.subcategory == filters['subcategory'])
                      # Special handling for phone queries - include all phone-related categories
                    user_query_lower = data['message'].lower()
                    if any(keyword in user_query_lower for keyword in ['phone', 'mobile', 'smartphone']):
                        category_conditions.extend([
                            Product.category == 'smartphones',
                            Product.subcategory == 'smartphones'
                        ])
                        
                        # For performance/flagship phones, include premium and gaming styles
                        if any(keyword in user_query_lower for keyword in ['performance', 'best', 'flagship', 'powerful', 'fast']):
                            category_conditions.extend([
                                Product.style == 'premium',
                                Product.style == 'gaming',
                                Product.subcategory == 'flagship'
                            ])
                    
                    # For casual/budget queries, show more product styles
                    if any(keyword in user_query_lower for keyword in ['casual', 'budget', 'cheap', 'affordable', 'low price']):
                        category_conditions.extend([
                            Product.style == 'budget',
                            Product.style == 'student',
                            Product.style == 'casual'
                        ])
                    
                    # Apply category conditions with OR logic (show if ANY condition matches)
                    if category_conditions:
                        query = query.filter(or_(*category_conditions))
                    
                    # Apply price filters (these are mandatory - use AND logic)
                    if filters.get('price_range'):
                        if filters['price_range'].get('min'):
                            query = query.filter(Product.price >= filters['price_range']['min'])
                        if filters['price_range'].get('max'):
                            query = query.filter(Product.price <= filters['price_range']['max'])
                    
                    # Execute query and get results
                    products = query.order_by(
                        Product.rating.desc(),
                        Product.stock_quantity.desc()
                    ).limit(20).all()
                    
                    # If no products found, fallback to broader search (remove category restrictions)
                    if not products:
                        fallback_query = Product.query
                        if filters.get('price_range'):
                            if filters['price_range'].get('min'):
                                fallback_query = fallback_query.filter(Product.price >= filters['price_range']['min'])
                            if filters['price_range'].get('max'):
                                fallback_query = fallback_query.filter(Product.price <= filters['price_range']['max'])
                        products = fallback_query.order_by(
                            Product.rating.desc(),
                            Product.stock_quantity.desc()
                        ).limit(10).all()
                
                product_list = [product.to_dict() for product in products]
                  # Generate intelligent response using Gemini
                response_msg = gemini_service.generate_response(
                    data['message'], 
                    product_list, 
                    history_list
                )
                
                # Generate smart suggestions for next questions
                suggestions = gemini_service.generate_suggestions(
                    data['message'],
                    product_list,
                    'product_recommendation'
                )
                
                # Store bot response
                bot_message = ChatMessage(
                    user_id=current_user_id,
                    message=response_msg,
                    is_bot=True,
                    session_id=session_id,
                    message_metadata={
                        'filters': filters,
                        'conversation_analysis': conversation_analysis,
                        'product_count': len(product_list),
                        'suggestions': suggestions
                    }
                )
                db.session.add(bot_message)
                db.session.commit()
                
                return jsonify({
                    'message': response_msg,
                    'session_id': session_id,
                    'products': product_list[:8],  # Return top 8 for display
                    'conversation_type': 'product_recommendation',                    'total_found': len(product_list),
                    'suggestions': suggestions
                })
            
            else:
                # General conversation or questions
                response_msg = gemini_service.generate_response(
                    data['message'], 
                    [], 
                    history_list
                )
                
                # Generate general help suggestions
                suggestions = [
                    "Help me find a laptop",
                    "Show me trending products", 
                    "What's on sale?",
                    "I need tech for work",
                    "Best gaming gear",
                    "Show me budget options"
                ]
                
                bot_message = ChatMessage(
                    user_id=current_user_id,
                    message=response_msg,
                    is_bot=True,
                    session_id=session_id,
                    message_metadata={
                        'conversation_analysis': conversation_analysis,
                        'suggestions': suggestions
                    }
                )
                db.session.add(bot_message)
                db.session.commit()
                
                return jsonify({
                    'message': response_msg,
                    'session_id': session_id,
                    'products': [],
                    'conversation_type': 'general_help',
                    'suggestions': suggestions
                })
            
        except Exception as e:
            db.session.rollback()
            print(f"Error processing message: {str(e)}")            # Fallback response
            fallback_msg = "Welcome to NexTechAI! 🚀 I'm Alex, your personal AI shopping assistant here to help you discover the perfect technology solutions from our premium electronics collection. What cutting-edge tech can I help you find today? We specialize in laptops, smartphones, gaming gear, audio equipment, and much more!"
            
            bot_message = ChatMessage(
                user_id=current_user_id,
                message=fallback_msg,
                is_bot=True,
                session_id=session_id,
                message_metadata={'error': 'processing_error'}
            )
            db.session.add(bot_message)
            db.session.commit()
            
            return jsonify({
                'message': fallback_msg,
                'session_id': session_id,
                'products': [],
                'conversation_type': 'error_recovery'
            })
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    try:
        current_user_id = get_jwt_identity()
        session_id = request.args.get('session_id')
        
        query = ChatMessage.query.filter_by(user_id=current_user_id)
        if session_id:
            query = query.filter_by(session_id=session_id)
        
        messages = query.order_by(ChatMessage.created_at.asc()).all()
        return jsonify({
            'messages': [message.to_dict() for message in messages]
        })
    except Exception as e:
        print(f"Error getting chat history: {str(e)}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_chat_sessions():
    try:
        current_user_id = get_jwt_identity()
        
        # Get unique session IDs with their latest message
        sessions = db.session.query(
            ChatMessage.session_id,
            db.func.max(ChatMessage.created_at).label('last_message_at')
        ).filter_by(user_id=current_user_id).group_by(ChatMessage.session_id).all()
        
        return jsonify([{
            'session_id': session[0],
            'last_message_at': session[1].isoformat()
        } for session in sessions])
    except Exception as e:
        print(f"Error getting chat sessions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history', methods=['DELETE'])
@jwt_required()
def clear_chat_history():
    try:
        current_user_id = get_jwt_identity()
        session_id = request.args.get('session_id')
        
        query = ChatMessage.query.filter_by(user_id=current_user_id)
        if session_id:
            query = query.filter_by(session_id=session_id)
        
        query.delete()
        db.session.commit()
        
        return jsonify({'message': 'Chat history cleared successfully'})
    except Exception as e:
        print(f"Error clearing chat history: {str(e)}")
        return jsonify({'error': str(e)}), 500