from datetime import datetime
from .user import db

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_bot = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(100))  # To group messages by conversation
    message_metadata = db.Column(db.JSON)  # Store additional data like product IDs, filters used, etc.
    
    def __init__(self, user_id, message, is_bot=False, session_id=None, message_metadata=None):
        self.user_id = user_id
        self.message = message
        self.is_bot = is_bot
        self.session_id = session_id
        self.message_metadata = message_metadata or {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'is_bot': self.is_bot,
            'created_at': self.created_at.isoformat(),
            'session_id': self.session_id,
            'message_metadata': self.message_metadata
        }
    
    def __repr__(self):
        return f'<ChatMessage {self.id}>'