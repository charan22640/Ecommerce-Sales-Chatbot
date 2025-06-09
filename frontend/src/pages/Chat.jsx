import React, { useState, useRef, useEffect } from 'react';
import { format } from 'date-fns';
import { 
  ChatBubbleLeftEllipsisIcon, 
  SparklesIcon, 
  LightBulbIcon,
  ArrowRightIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline';
import api from '../services/api';
import ProductCard from '../components/ProductCard';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const messagesEndRef = useRef(null);

  // Dynamic suggestion system
  const generateSuggestions = (lastMessage, conversationType, products = []) => {
    if (!lastMessage || !lastMessage.is_bot) return [];

    const messageText = lastMessage.message.toLowerCase();
    const hasProducts = products && products.length > 0;

    // Base suggestions that are always relevant
    const baseSuggestions = [
      "Show me more options",
      "What's your best recommendation?",
      "Compare the top 3 products"
    ];

    // Context-specific suggestions
    let contextSuggestions = [];

    if (conversationType === 'greeting') {
      contextSuggestions = [
        "I need a laptop for work",
        "Show me gaming headphones",
        "Looking for a smartphone",
        "Best tablets for students",
        "Wireless earbuds under $100"
      ];
    } else if (conversationType === 'product_recommendation' && hasProducts) {
      const categories = [...new Set(products.map(p => p.category))];
      const priceRanges = products.map(p => p.price);
      const minPrice = Math.min(...priceRanges);
      const maxPrice = Math.max(...priceRanges);

      contextSuggestions = [
        "Tell me more about the first product",
        `Show me ${categories[0]} under $${Math.round(maxPrice * 0.8)}`,
        "What's the difference between these models?",
        "Which one has the best reviews?",
        "Show me premium options",
        "Any budget alternatives?"
      ];

      // Category-specific suggestions
      if (categories.includes('smartphones')) {
        contextSuggestions.push(
          "Which has the best camera?",
          "Show me phones with long battery life",
          "Any 5G compatible models?"
        );
      }
      
      if (categories.includes('audio') || categories.includes('gaming')) {
        contextSuggestions.push(
          "Which has the best sound quality?",
          "Any noise-canceling options?",
          "Show me wireless models"
        );
      }

      if (categories.includes('laptops') || categories.includes('computers')) {
        contextSuggestions.push(
          "Which is best for gaming?",
          "Show me lightweight options",
          "Any 2-in-1 convertibles?"
        );
      }
    } else if (conversationType === 'clarification') {
      if (messageText.includes('non-electronics')) {
        contextSuggestions = [
          "Show me laptops instead",
          "I need smartphones",
          "Looking for headphones",
          "Show me tablets",
          "Any gaming accessories?"
        ];
      } else {
        contextSuggestions = [
          "I'm looking for laptops",
          "Show me smartphones",
          "Need gaming headphones",
          "Looking for tablets under $500",
          "Best wireless earbuds"
        ];
      }
    } else {
      // General conversation suggestions
      contextSuggestions = [
        "Help me find a laptop",
        "Show me trending products",
        "What's on sale?",
        "I need tech for work",
        "Best gaming gear"
      ];
    }

    // Combine and randomize suggestions
    const allSuggestions = [...contextSuggestions, ...baseSuggestions];
    return allSuggestions.slice(0, 6); // Limit to 6 suggestions
  };

  // Initial conversation starters
  const conversationStarters = [
    "Hi! I'm looking for a new laptop for work",
    "Show me gaming headphones under $200", 
    "I need a smartphone with good camera",
    "What are the best wireless earbuds?",
    "Looking for a tablet for my studies",
    "Show me trending electronics"
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  // Add welcome message when component loads
  useEffect(() => {
    if (messages.length === 0) {      const welcomeMessage = {
        message: "Welcome to NexTechAI! 🚀\n\nI'm Alex, your personal AI shopping assistant at NexTechAI - your premier destination for cutting-edge electronics and smart technology solutions.\n\nAt NexTechAI, we specialize in the latest smartphones, powerful laptops, immersive gaming gear, premium audio equipment, and innovative smart devices. Our AI-powered platform ensures you find exactly what you need.\n\nHow can I help you discover the perfect tech today?",
        is_bot: true,
        created_at: new Date().toISOString(),
        products: [],
        conversation_type: 'greeting'
      };
      setMessages([welcomeMessage]);
      setSuggestions(generateSuggestions(welcomeMessage, 'greeting'));
    }
  }, []);
  // Update suggestions when messages change
  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.is_bot) {
        // Use backend suggestions if available, otherwise generate frontend suggestions
        const backendSuggestions = lastMessage.suggestions;
        if (backendSuggestions && backendSuggestions.length > 0) {
          setSuggestions(backendSuggestions);
        } else {
          const newSuggestions = generateSuggestions(
            lastMessage, 
            lastMessage.conversation_type, 
            lastMessage.products
          );
          setSuggestions(newSuggestions);
        }
      }
    }
  }, [messages]);
  const handleSubmit = async (e, suggestionText = null) => {
    e.preventDefault();
    const messageText = suggestionText || input.trim();
    if (!messageText || loading) return;

    if (!suggestionText) setInput('');
    setLoading(true);

    // Add user message to chat
    setMessages(prev => [...prev, {
      message: messageText,
      is_bot: false,
      created_at: new Date().toISOString(),
      products: []
    }]);

    // Clear suggestions temporarily while loading
    setSuggestions([]);

    try {
      const response = await api.post('/chat/message', {
        message: messageText,
        session_id: sessionId
      });

      // Update session ID if it's a new conversation
      if (!sessionId) {
        setSessionId(response.data.session_id);
      }      // Add bot response to chat
      const botMessage = {
        message: response.data.message,
        is_bot: true,
        created_at: new Date().toISOString(),
        products: response.data.products || [],
        conversation_type: response.data.conversation_type || 'general',
        total_found: response.data.total_found || 0,
        suggestions: response.data.suggestions || []
      };

      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        message: 'Sorry, I encountered an error. Please try again.',
        is_bot: true,
        created_at: new Date().toISOString(),
        products: []
      }]);
    } finally {
      setLoading(false);
    }
  };
  const handleStarterClick = (starter) => {
    setInput(starter);
  };

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
    // Auto-submit the suggestion
    setTimeout(() => {
      handleSubmit({ preventDefault: () => {} }, suggestion);
    }, 100);
  };
  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-gray-50">
      {/* Chat Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <ChatBubbleLeftEllipsisIcon className="w-6 h-6 text-white" />
            </div>            <div>              <h1 className="text-lg font-semibold text-gray-900">Alex - NexTechAI Assistant</h1>
              <p className="text-sm text-gray-600 flex items-center">
                <SparklesIcon className="w-4 h-4 mr-1" />
                NexTechAI - Smart Electronics Shopping
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.is_bot ? 'justify-start' : 'justify-end'}`}
          >
            <div className={`max-w-[80%] ${msg.is_bot ? 'mr-auto' : 'ml-auto'}`}>
              {/* Message Bubble */}
              <div
                className={`rounded-2xl px-4 py-3 ${
                  msg.is_bot
                    ? 'bg-white text-gray-800 border border-gray-200 shadow-sm'
                    : 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
                }`}
              >
                {msg.is_bot && (
                  <div className="flex items-center mb-2">
                    <div className="w-6 h-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mr-2">
                      <span className="text-xs text-white font-bold">A</span>
                    </div>
                    <span className="text-sm font-medium text-gray-700">Alex</span>
                    {msg.conversation_type && (
                      <span className={`ml-2 px-2 py-1 text-xs rounded-full ${
                        msg.conversation_type === 'product_recommendation' ? 'bg-green-100 text-green-800' :
                        msg.conversation_type === 'greeting' ? 'bg-blue-100 text-blue-800' :
                        msg.conversation_type === 'clarification' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {msg.conversation_type.replace('_', ' ')}
                      </span>
                    )}
                  </div>
                )}
                
                <p className="whitespace-pre-wrap leading-relaxed">{msg.message}</p>
                
                {/* Show product count if applicable */}
                {msg.is_bot && msg.total_found > 0 && (
                  <div className="mt-2 text-sm text-gray-600">
                    Found {msg.total_found} product{msg.total_found !== 1 ? 's' : ''} matching your criteria
                  </div>
                )}
                
                <div className="flex justify-between items-center mt-2">
                  <span className={`text-xs ${msg.is_bot ? 'text-gray-500' : 'text-blue-100'}`}>
                    {format(new Date(msg.created_at), 'HH:mm')}
                  </span>
                </div>
              </div>              {/* Products Grid */}
              {msg.is_bot && msg.products && msg.products.length > 0 && (
                <div className="mt-4">
                  <div className="text-sm font-medium text-gray-700 mb-3 flex items-center">
                    <SparklesIcon className="w-4 h-4 mr-1" />
                    Recommended Products
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    {msg.products.map((product) => (
                      <div key={product.id} className="transform hover:scale-105 transition-transform duration-200">
                        <ProductCard product={product} />
                      </div>
                    ))}
                  </div>
                </div>
              )}              {/* Smart Suggestions - show for the latest bot message */}
              {msg.is_bot && idx === messages.length - 1 && !loading && suggestions.length > 0 && (
                <div className="mt-4 animate-fade-in">
                  <div className="text-sm font-medium text-gray-700 mb-3 flex items-center">
                    <LightBulbIcon className="w-4 h-4 mr-1 text-amber-500 animate-pulse" />
                    <span className="bg-gradient-to-r from-amber-500 to-orange-500 bg-clip-text text-transparent">
                      Suggested Questions
                    </span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {suggestions.map((suggestion, suggestionIdx) => (
                      <button
                        key={suggestionIdx}
                        onClick={() => handleSuggestionClick(suggestion)}
                        className="suggestion-card group flex items-center justify-between p-3 text-left bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 hover:from-blue-100 hover:via-indigo-100 hover:to-purple-100 border border-blue-200 hover:border-indigo-300 rounded-xl transition-all duration-300 hover:shadow-lg hover:scale-105 transform"
                        style={{ animationDelay: `${suggestionIdx * 0.1}s` }}
                      >
                        <span className="text-sm text-gray-700 group-hover:text-gray-900 flex-1 font-medium">
                          {suggestion}
                        </span>
                        <ArrowRightIcon className="w-4 h-4 text-blue-400 group-hover:text-indigo-600 opacity-0 group-hover:opacity-100 transition-all duration-300 transform group-hover:translate-x-1" />
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
          {loading && (
          <div className="flex justify-start">
            <div className="max-w-[80%] mr-auto">
              <div className="bg-white text-gray-800 border border-gray-200 shadow-sm rounded-2xl px-4 py-3 animate-pulse">
                <div className="flex items-center space-x-2">
                  <div className="w-6 h-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-xs text-white font-bold">A</span>
                  </div>
                  <span className="text-sm font-medium text-gray-700">Alex is thinking...</span>
                </div>
                <div className="flex space-x-1 mt-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>      {/* Conversation Starters (show only when no messages except welcome and no suggestions) */}
      {messages.length === 1 && suggestions.length === 0 && (
        <div className="px-6 pb-4">
          <div className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <MagnifyingGlassIcon className="w-4 h-4 mr-1" />
            Popular searches:
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">            {conversationStarters.map((starter, idx) => (
              <button
                key={idx}
                onClick={() => handleStarterClick(starter)}
                className="group flex items-center justify-between p-4 text-left bg-white border border-gray-200 rounded-xl hover:border-blue-300 hover:shadow-lg hover:scale-105 transition-all duration-300 transform"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <span className="text-sm text-gray-700 group-hover:text-gray-900 flex-1 font-medium">
                  {starter}
                </span>
                <ArrowRightIcon className="w-4 h-4 text-gray-300 group-hover:text-blue-500 opacity-0 group-hover:opacity-100 transition-all duration-300 transform group-hover:translate-x-1" />
              </button>
            ))}
          </div>
        </div>
      )}      {/* Quick Actions Bar - Always visible when not loading */}
      {!loading && messages.length > 1 && (
        <div className="px-6 pb-2">
          <div className="flex flex-wrap gap-2 justify-center">
            <button
              onClick={() => handleSuggestionClick("Show me trending smartphones and laptops")}
              className="px-3 py-1.5 text-xs bg-gradient-to-r from-green-50 to-emerald-50 text-green-700 border border-green-200 rounded-full hover:from-green-100 hover:to-emerald-100 hover:scale-105 transition-all duration-200 animate-pulse"
            >
              🔥 Trending
            </button>
            <button
              onClick={() => handleSuggestionClick("Show me discounted electronics under $500")}
              className="px-3 py-1.5 text-xs bg-gradient-to-r from-red-50 to-pink-50 text-red-700 border border-red-200 rounded-full hover:from-red-100 hover:to-pink-100 hover:scale-105 transition-all duration-200"
            >
              💰 Deals
            </button>
            <button
              onClick={() => handleSuggestionClick("Show me premium electronics above $800")}
              className="px-3 py-1.5 text-xs bg-gradient-to-r from-purple-50 to-indigo-50 text-purple-700 border border-purple-200 rounded-full hover:from-purple-100 hover:to-indigo-100 hover:scale-105 transition-all duration-200"
            >
              ⭐ Premium
            </button>
            <button
              onClick={() => handleSuggestionClick("Show me budget electronics under $200")}
              className="px-3 py-1.5 text-xs bg-gradient-to-r from-blue-50 to-cyan-50 text-blue-700 border border-blue-200 rounded-full hover:from-blue-100 hover:to-cyan-100 hover:scale-105 transition-all duration-200"
            >
              💡 Budget
            </button>
          </div>
        </div>
      )}{/* Chat Input */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        {/* Input suggestions preview */}
        {input.length > 2 && suggestions.length > 0 && !loading && (
          <div className="mb-3">
            <div className="text-xs text-gray-500 mb-2">Quick suggestions:</div>
            <div className="flex flex-wrap gap-2">
              {suggestions.slice(0, 3).map((suggestion, idx) => (
                <button
                  key={idx}
                  onClick={() => setInput(suggestion)}
                  className="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-md transition-colors duration-150"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="flex space-x-4">
          <div className="flex-1 relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Discover NexTechAI's premium electronics collection..."
              className="w-full px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 pr-12"
              disabled={loading}
            />
            {input && (
              <button
                type="button"
                onClick={() => setInput('')}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            )}
          </div>
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-full hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-medium shadow-lg hover:shadow-xl"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <span className="flex items-center">
                Send
                <ArrowRightIcon className="w-4 h-4 ml-1" />
              </span>
            )}
          </button>
        </form>
        
        {/* Typing indicator for suggestions */}
        {!loading && suggestions.length > 0 && (
          <div className="mt-2 text-xs text-gray-400 text-center">
            💡 Tap any suggestion above for instant answers
          </div>
        )}
      </div>
    </div>
  );
}