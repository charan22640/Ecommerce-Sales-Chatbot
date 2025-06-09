# E-commerce Sales Chatbot

A sophisticated e-commerce sales chatbot that enhances the shopping experience by enabling efficient product search, exploration, and purchase processes. The system features a responsive web interface and a powerful backend API that processes user queries and manages product data.

## 🌟 Features

- **Intelligent Chatbot Interface**
  - Natural language processing for product queries
  - Context-aware conversations
  - Product recommendations
  - Shopping cart management
  - Order processing assistance

- **User Authentication**
  - Secure login/signup system
  - JWT-based authentication
  - Session management
  - User profile management

- **Product Management**
  - Rich product catalog with 100+ items
  - Advanced search and filtering
  - Product categorization
  - Image handling
  - Price and inventory tracking

- **Shopping Experience**
  - Real-time cart updates
  - Secure checkout process
  - Order history
  - Product reviews and ratings

## 🛠️ Technology Stack

### Frontend
- React.js with TypeScript
- Tailwind CSS for styling
- Axios for API communication
- React Router for navigation
- Context API for state management

### Backend
- Python 3.8+
- Flask framework
- SQLAlchemy ORM
- PostgreSQL database
- JWT for authentication
- Flask-CORS for cross-origin support

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 14.x or higher
- PostgreSQL 12 or higher
- npm or yarn package manager

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ecommercesalesbot.git
   cd ecommercesalesbot
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb ecommerce_db
   
   # Run migrations
   flask db upgrade
   
   # Seed the database with sample data
   python seed_enhanced_db.py
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

## ⚙️ Configuration

1. **Backend Environment Variables**
   Create a `.env` file in the backend directory:
   ```
   FLASK_APP=wsgi.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://localhost/ecommerce_db
   JWT_SECRET_KEY=your-secret-key
   ```

2. **Frontend Environment Variables**
   Create a `.env` file in the frontend directory:
   ```
   REACT_APP_API_URL=http://localhost:5000
   ```

## 🏃‍♂️ Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   flask run
   ```

2. **Start the Frontend Development Server**
   ```bash
   cd frontend
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 📚 API Documentation

### Authentication Endpoints
- POST /api/auth/register - User registration
- POST /api/auth/login - User login
- GET /api/auth/profile - Get user profile

### Product Endpoints
- GET /api/products - List all products
- GET /api/products/<id> - Get product details
- GET /api/products/search - Search products

### Cart Endpoints
- GET /api/cart - Get user's cart
- POST /api/cart/items - Add item to cart
- PUT /api/cart/items/<id> - Update cart item
- DELETE /api/cart/items/<id> - Remove item from cart

### Order Endpoints
- POST /api/orders - Create new order
- GET /api/orders - List user's orders
- GET /api/orders/<id> - Get order details

## 🧪 Testing

Run the test suite:
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Deployment

### Backend Deployment
1. Set up a production PostgreSQL database
2. Configure environment variables for production
3. Use Gunicorn as the WSGI server
4. Set up Nginx as a reverse proxy

### Frontend Deployment
1. Build the production bundle:
   ```bash
   cd frontend
   npm run build
   ```
2. Deploy the build folder to your web server

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Flask documentation
- React documentation
- PostgreSQL documentation
- All contributors who have helped shape this project

## 📞 Support

For support, email your-email@example.com or create an issue in the repository. 