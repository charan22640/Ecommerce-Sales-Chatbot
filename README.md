# E-commerce Sales Chatbot

A full-stack, production-ready E-commerce Sales Chatbot for the clothing category, powered by Google Gemini AI.

## 🚀 Features

- **Smart Chatbot Interface**: Natural language processing for product queries
- **User Authentication**: Secure JWT-based authentication system
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Intelligent Product Search**: Powered by Google Gemini AI
- **Real-time Chat**: Interactive product browsing experience
- **Session Management**: Persistent chat history and user sessions

## 🛠️ Tech Stack

- **Frontend**: Vite + React + Tailwind CSS
- **Backend**: Python Flask
- **Database**: SQLite (with SQLAlchemy ORM)
- **AI Integration**: Google Gemini API
- **Authentication**: JWT

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Google Cloud Account (for Gemini API)
- SQLite3

## 🚀 Getting Started

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Gemini API key and other configurations
```

4. Initialize database:
```bash
flask db upgrade
flask seed-db  # Populates mock data
```

5. Run the backend server:
```bash
flask run
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env
```

3. Run development server:
```bash
npm run dev
```

## 📁 Project Structure

```
ecommercesalesbot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── migrations/
│   ├── tests/
│   └── config.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── public/
└── README.md
```

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Products
- `GET /api/products` - List products with filters
- `GET /api/products/:id` - Get product details

### Chat
- `POST /api/chat/message` - Send message to chatbot
- `GET /api/chat/history` - Get chat history
- `DELETE /api/chat/history` - Clear chat history

## 🤖 Sample Queries

The chatbot understands natural language queries like:
- "Show me stylish kurtis under ₹1000"
- "I need jeans for a party"
- "Find me something casual and blue"

## 🔒 Security

- JWT-based authentication
- Secure password hashing
- API key management
- Input validation and sanitization

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 License

MIT

## 👥 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 