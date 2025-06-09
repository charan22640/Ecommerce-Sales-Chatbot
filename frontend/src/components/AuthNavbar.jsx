import React from 'react';
import { Link } from 'react-router-dom';

const AuthNavbar = () => {
  return (
    <nav className="bg-white shadow-lg border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-3">
            <Link to="/" className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-2">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  NexTechAI
                </h1>
                <p className="text-xs text-gray-500 -mt-1">Smart Shopping Assistant</p>
              </div>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium">
              Home
            </Link>
            <Link to="/products" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium">
              Products
            </Link>
            <Link to="/chat" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium">
              AI Assistant
            </Link>
            <div className="h-6 w-px bg-gray-300"></div>
            <div className="flex items-center space-x-4">
              <Link 
                to="/login" 
                className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium"
              >
                Sign In
              </Link>
              <Link 
                to="/register" 
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 font-medium shadow-md hover:shadow-lg"
              >
                Get Started
              </Link>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button className="text-gray-600 hover:text-blue-600 transition-colors duration-200">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default AuthNavbar;
