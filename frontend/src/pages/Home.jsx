import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  SparklesIcon, 
  ChatBubbleLeftRightIcon,
  ShoppingBagIcon,
  LightBulbIcon,
  RocketLaunchIcon,
  DevicePhoneMobileIcon,
  ComputerDesktopIcon,
  SpeakerWaveIcon,
  PlayIcon,
  StarIcon,
  ArrowRightIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

export default function Home() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [currentTestimonial, setCurrentTestimonial] = useState(0);

  const features = [
    {
      icon: SparklesIcon,
      title: "AI-Powered Recommendations",
      description: "Get personalized product suggestions based on your preferences and needs with our advanced AI technology.",
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: ChatBubbleLeftRightIcon,
      title: "Smart Chat Assistant",
      description: "Talk to Alex, our AI shopping assistant, in natural language to find exactly what you're looking for.",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: LightBulbIcon,
      title: "Intelligent Search",
      description: "Our AI understands context and intent, making it easier to discover products you'll love.",
      color: "from-green-500 to-emerald-500"
    },
    {
      icon: RocketLaunchIcon,
      title: "Lightning Fast",
      description: "Get instant responses and product recommendations powered by cutting-edge AI technology.",
      color: "from-orange-500 to-red-500"
    }
  ];

  const categories = [
    {
      icon: DevicePhoneMobileIcon,
      title: "Smartphones",
      description: "Latest flagship and budget phones",
      products: "250+ products",
      color: "bg-blue-50 border-blue-200"
    },
    {
      icon: ComputerDesktopIcon,
      title: "Laptops",
      description: "Gaming, work, and study laptops",
      products: "180+ products",
      color: "bg-purple-50 border-purple-200"
    },
    {
      icon: SpeakerWaveIcon,
      title: "Audio",
      description: "Headphones, speakers, and earbuds",
      products: "320+ products",
      color: "bg-green-50 border-green-200"
    }
  ];

  const testimonials = [
    {
      name: "Sarah Johnson",
      role: "Tech Enthusiast",
      content: "NexTechAI found me the perfect laptop for my needs. The AI recommendations were spot-on!",
      rating: 5,
      avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b5bc?w=64&h=64&fit=crop&crop=face"
    },
    {
      name: "Mike Chen",
      role: "Developer",
      content: "The chat assistant is incredible. It understood exactly what I needed for my home office setup.",
      rating: 5,
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=64&h=64&fit=crop&crop=face"
    },
    {
      name: "Emily Rodriguez",
      role: "Student",
      content: "Found amazing deals on electronics. The AI helped me stay within my budget while getting quality products.",
      rating: 5,
      avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=64&h=64&fit=crop&crop=face"
    }
  ];

  const stats = [
    { label: "Happy Customers", value: "10,000+", icon: "👥" },
    { label: "Products Available", value: "50,000+", icon: "📱" },
    { label: "AI Recommendations", value: "1M+", icon: "🤖" },
    { label: "Customer Satisfaction", value: "98%", icon: "⭐" }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleStartShopping = () => {
    navigate('/chat');
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Content */}
            <div className="text-center lg:text-left">
              <div className="inline-flex items-center bg-blue-100 text-blue-800 text-sm font-medium px-4 py-2 rounded-full mb-6">
                <SparklesIcon className="w-4 h-4 mr-2" />
                AI-Powered Shopping Experience
              </div>
              
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
                Shop Smarter with{' '}
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AI Technology
                </span>
              </h1>
              
              <p className="text-xl text-gray-600 mb-8 max-w-2xl">
                Meet Alex, your personal AI shopping assistant. Get instant product recommendations, 
                compare prices, and discover the perfect electronics for your needs.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <button
                  onClick={handleStartShopping}
                  className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
                >
                  <ChatBubbleLeftRightIcon className="w-5 h-5 mr-2" />
                  Start Shopping with AI
                  <ArrowRightIcon className="w-5 h-5 ml-2" />
                </button>
                
                <Link
                  to="/products"
                  className="inline-flex items-center px-8 py-4 bg-white text-gray-700 font-semibold rounded-xl border-2 border-gray-200 hover:border-blue-300 hover:text-blue-600 transition-all duration-200 shadow-md hover:shadow-lg"
                >
                  <ShoppingBagIcon className="w-5 h-5 mr-2" />
                  Browse Products
                </Link>
              </div>

              {/* Trust Indicators */}
              <div className="flex items-center justify-center lg:justify-start space-x-6 mt-8 text-sm text-gray-500">
                <div className="flex items-center">
                  <CheckCircleIcon className="w-5 h-5 text-green-500 mr-2" />
                  Free shipping
                </div>
                <div className="flex items-center">
                  <CheckCircleIcon className="w-5 h-5 text-green-500 mr-2" />
                  30-day returns
                </div>
                <div className="flex items-center">
                  <CheckCircleIcon className="w-5 h-5 text-green-500 mr-2" />
                  Secure payments
                </div>
              </div>
            </div>

            {/* Right Column - Visual */}
            <div className="relative">
              <div className="relative z-10">
                {/* Chat Preview */}
                <div className="bg-white rounded-2xl shadow-2xl p-6 max-w-md mx-auto">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mr-3">
                      <SparklesIcon className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Alex AI Assistant</h3>
                      <p className="text-sm text-green-500">● Online</p>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="bg-gray-100 rounded-lg p-3">
                      <p className="text-sm text-gray-600">Hi! I'm looking for a gaming laptop under $1500</p>
                    </div>
                    <div className="bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg p-3">
                      <p className="text-sm">Perfect! I found 3 excellent gaming laptops within your budget. The ASUS ROG Strix G15 looks ideal for your needs...</p>
                    </div>
                  </div>
                  
                  <div className="mt-4 flex space-x-2">
                    <div className="flex-1 bg-gray-100 rounded-lg p-2 text-center">
                      <p className="text-xs text-gray-600">Tell me more</p>
                    </div>
                    <div className="flex-1 bg-gray-100 rounded-lg p-2 text-center">
                      <p className="text-xs text-gray-600">Show alternatives</p>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Background Elements */}
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-blue-200 rounded-full opacity-20 animate-pulse"></div>
              <div className="absolute -bottom-8 -left-8 w-32 h-32 bg-purple-200 rounded-full opacity-20 animate-pulse delay-1000"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Why Choose NexTechAI?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experience the future of online shopping with our cutting-edge AI technology
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100"
              >
                <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-xl flex items-center justify-center mb-6`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Shop by Category
            </h2>
            <p className="text-xl text-gray-600">
              Discover our wide range of premium electronics
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {categories.map((category, index) => (
              <Link
                key={index}
                to="/products"
                className={`${category.color} rounded-2xl p-8 border-2 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 group`}
              >
                <category.icon className="w-12 h-12 text-gray-700 mb-4 group-hover:scale-110 transition-transform duration-200" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{category.title}</h3>
                <p className="text-gray-600 mb-3">{category.description}</p>
                <p className="text-sm font-medium text-blue-600">{category.products}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-24 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
            {stats.map((stat, index) => (
              <div key={index} className="text-white">
                <div className="text-4xl mb-2">{stat.icon}</div>
                <div className="text-3xl sm:text-4xl font-bold mb-2">{stat.value}</div>
                <div className="text-blue-100">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              What Our Customers Say
            </h2>
            <p className="text-xl text-gray-600">
              Join thousands of satisfied customers
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-8 lg:p-12">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  {[...Array(5)].map((_, i) => (
                    <StarIcon key={i} className="w-6 h-6 text-yellow-400 fill-current" />
                  ))}
                </div>
                
                <blockquote className="text-xl lg:text-2xl text-gray-700 mb-8">
                  "{testimonials[currentTestimonial].content}"
                </blockquote>
                
                <div className="flex items-center justify-center">
                  <img
                    className="w-12 h-12 rounded-full mr-4"
                    src={testimonials[currentTestimonial].avatar}
                    alt={testimonials[currentTestimonial].name}
                  />
                  <div className="text-left">
                    <div className="font-semibold text-gray-900">
                      {testimonials[currentTestimonial].name}
                    </div>
                    <div className="text-gray-600">
                      {testimonials[currentTestimonial].role}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Testimonial Dots */}
            <div className="flex justify-center mt-8 space-x-2">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentTestimonial(index)}
                  className={`w-3 h-3 rounded-full transition-colors duration-200 ${
                    index === currentTestimonial ? 'bg-blue-600' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6">
              Ready to Start Your AI Shopping Journey?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Join thousands of customers who trust NexTechAI for their electronics needs
            </p>
            <button
              onClick={handleStartShopping}
              className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
            >
              <ChatBubbleLeftRightIcon className="w-5 h-5 mr-2" />
              Start Shopping Now
              <ArrowRightIcon className="w-5 h-5 ml-2" />
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
