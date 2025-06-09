from app import create_app, db
from app.models.chat import ChatMessage
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError

def test_chat():
    app = create_app()
    with app.app_context():
        try:
            # Create test user if not exists
            user = User.query.first()
            if not user:
                user = User(username='test', email='test@example.com', password='test123')
                db.session.add(user)
                db.session.commit()
                print(f"Created new user with ID: {user.id}")
            else:
                print(f"Using existing user with ID: {user.id}")
            
            # Create a test message
            message = ChatMessage(
                user_id=user.id,
                message='Show me some blue jeans',
                is_bot=False,
                session_id='test_session',
                message_metadata={'category': 'jeans', 'color': 'blue'}
            )
            db.session.add(message)
            db.session.commit()
            
            # Verify the message was stored correctly
            stored_message = message.to_dict()
            print('\nStored message:')
            print(stored_message)
            
            # Verify the message_metadata field
            print('\nMessage metadata:')
            print(stored_message.get('message_metadata'))
            
            # Clean up the test message
            db.session.delete(message)
            db.session.commit()
            print('\nTest message cleaned up')
            
        except SQLAlchemyError as e:
            print(f"Database error occurred: {str(e)}")
            db.session.rollback()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    test_chat()
