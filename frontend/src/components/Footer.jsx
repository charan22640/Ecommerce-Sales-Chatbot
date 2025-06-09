import React from 'react';
import { Link } from 'react-router-dom';
import { 
  HeartIcon, 
  ShieldCheckIcon, 
  TruckIcon, 
  ChatBubbleLeftRightIcon,
  EnvelopeIcon,
  PhoneIcon,
  MapPinIcon
} from '@heroicons/react/24/outline';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white">
      {/* Main Footer Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="lg:col-span-1">
            <Link to="/" className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-lg">N</span>
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                NexTechAI
              </span>
            </Link>
            <p className="text-gray-300 mb-4 leading-relaxed">
              Your premier destination for cutting-edge electronics and smart technology solutions. 
              Discover the future of tech with AI-powered shopping assistance.
            </p>
            <div className="flex space-x-3">
              <div className="flex items-center text-green-400">
                <ShieldCheckIcon className="w-5 h-5 mr-2" />
                <span className="text-sm">Secure Shopping</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-blue-400">Quick Links</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/products" className="text-gray-300 hover:text-blue-400 transition-colors duration-200 flex items-center">
                  <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity"></span>
                  All Products
                </Link>
              </li>
              <li>
                <Link to="/cart" className="text-gray-300 hover:text-blue-400 transition-colors duration-200 flex items-center">
                  <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity"></span>
                  Shopping Cart
                </Link>
              </li>
              <li>
                <Link to="/orders" className="text-gray-300 hover:text-blue-400 transition-colors duration-200 flex items-center">
                  <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mr-2 opacity-0 group-hover:opacity-100 transition-opacity"></span>
                  Order History
                </Link>
              </li>
              <li>
                <Link to="/" className="text-gray-300 hover:text-blue-400 transition-colors duration-200 flex items-center">
                  <ChatBubbleLeftRightIcon className="w-4 h-4 mr-2" />
                  AI Assistant
                </Link>
              </li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-purple-400">Categories</h3>
            <ul className="space-y-3">
              <li>
                <button className="text-gray-300 hover:text-purple-400 transition-colors duration-200 text-left">
                  📱 Smartphones
                </button>
              </li>
              <li>
                <button className="text-gray-300 hover:text-purple-400 transition-colors duration-200 text-left">
                  💻 Laptops
                </button>
              </li>
              <li>
                <button className="text-gray-300 hover:text-purple-400 transition-colors duration-200 text-left">
                  🎧 Audio Equipment
                </button>
              </li>
              <li>
                <button className="text-gray-300 hover:text-purple-400 transition-colors duration-200 text-left">
                  🎮 Gaming Gear
                </button>
              </li>
              <li>
                <button className="text-gray-300 hover:text-purple-400 transition-colors duration-200 text-left">
                  📺 Smart Devices
                </button>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-green-400">Contact Us</h3>
            <div className="space-y-3">
              <div className="flex items-center text-gray-300">
                <MapPinIcon className="w-5 h-5 mr-3 text-green-400" />
                <span className="text-sm">Silicon Valley, CA</span>
              </div>
              <div className="flex items-center text-gray-300">
                <PhoneIcon className="w-5 h-5 mr-3 text-green-400" />
                <span className="text-sm">+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center text-gray-300">
                <EnvelopeIcon className="w-5 h-5 mr-3 text-green-400" />
                <span className="text-sm">support@nextechai.com</span>
              </div>
              <div className="flex items-center text-blue-400 mt-4 p-3 bg-blue-900/30 rounded-lg border border-blue-800">
                <ChatBubbleLeftRightIcon className="w-5 h-5 mr-2" />
                <span className="text-sm font-medium">24/7 AI Support Available</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Bar */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex items-center justify-center text-center">
              <TruckIcon className="w-6 h-6 text-blue-400 mr-3" />
              <div>
                <div className="font-semibold text-white">Free Shipping</div>
                <div className="text-sm text-gray-400">On orders over $50</div>
              </div>
            </div>
            <div className="flex items-center justify-center text-center">
              <ShieldCheckIcon className="w-6 h-6 text-green-400 mr-3" />
              <div>
                <div className="font-semibold text-white">Secure Payment</div>
                <div className="text-sm text-gray-400">256-bit SSL encryption</div>
              </div>
            </div>
            <div className="flex items-center justify-center text-center">
              <ChatBubbleLeftRightIcon className="w-6 h-6 text-purple-400 mr-3" />
              <div>
                <div className="font-semibold text-white">AI Assistant</div>
                <div className="text-sm text-gray-400">Smart product recommendations</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800 bg-gray-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm text-gray-400 mb-2 md:mb-0">
              © {currentYear} NexTechAI. All rights reserved. 
              <span className="mx-2">|</span>
              <button className="hover:text-gray-300 transition-colors">Privacy Policy</button>
              <span className="mx-2">|</span>
              <button className="hover:text-gray-300 transition-colors">Terms of Service</button>
            </div>
            <div className="flex items-center text-sm text-gray-400">
              Made with 
              <HeartIcon className="w-4 h-4 text-red-500 mx-1" />
              by NexTechAI Team
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
