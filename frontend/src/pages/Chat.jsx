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
  };  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  // Add welcome message when component loads
  useEffect(() => {
    if (messages.length === 0) {      
      // Add small delay for animation effect
      setTimeout(() => {
        const welcomeMessage = {
          message: "Welcome to NexTechAI! 🚀\n\nI'm Alex, your personal AI shopping assistant at NexTechAI - your premier destination for cutting-edge electronics and smart technology solutions.\n\nAt NexTechAI, we specialize in the latest smartphones, powerful laptops, immersive gaming gear, premium audio equipment, and innovative smart devices.\n\nHow can I help you discover the perfect tech today?",
          is_bot: true,
          created_at: new Date().toISOString(),
          products: [],
          conversation_type: 'greeting'
        };
        setMessages([welcomeMessage]);
        setSuggestions(generateSuggestions(welcomeMessage, 'greeting'));
      }, 300);
    }
  }, []);
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

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
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
  };  return (
    <div className="h-full w-full">      {/* Fixed Chat Container without extra navbar */}
      <div className="chat-container chat-container-with-sliding-navbar animate-fade-in flex flex-col w-full bg-white/95 backdrop-blur-sm overflow-hidden">
        {/* Fixed Messages Container with proper scrolling */}        <div className="flex-1 overflow-hidden flex flex-col w-full">
          <div className="chat-messages-container flex-1 overflow-y-auto px-4 py-6 space-y-5 chat-scroll min-h-[calc(100vh-125px)] w-full">
            {messages.length === 0 && (
              <div className="flex items-center justify-center h-full">
                <div className="text-center p-8 rounded-2xl bg-gradient-to-r from-slate-50 to-blue-50 border border-blue-100 shadow-inner max-w-lg">                  <div className="flex items-center justify-center mb-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                      <ChatBubbleLeftEllipsisIcon className="w-8 h-8 text-white" />
                    </div>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">Welcome to NexTechAI Assistant</h3>
                  <div className="flex items-center justify-center gap-3 mb-4">
                    <div className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full border border-green-200 flex items-center">
                      <div className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1 animate-pulse"></div>
                      Alex is Online
                    </div>
                    <div className="text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded-full border border-blue-200 flex items-center">
                      <SparklesIcon className="w-3 h-3 mr-1" />
                      AI Recommendations
                    </div>
                  </div>
                  <p className="text-gray-600 mb-6">I'm here to help you find the perfect electronics for your needs. Feel free to ask me about products or recommendations!</p>
                  <div className="grid grid-cols-2 gap-3">
                    <button onClick={() => handleSuggestionClick("What are your best selling laptops?")} 
                      className="px-4 py-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100 text-blue-600 hover:shadow-md transition-all">
                      Popular Laptops
                    </button>
                    <button onClick={() => handleSuggestionClick("Show me gaming headphones under $100")} 
                      className="px-4 py-3 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl border border-indigo-100 text-indigo-600 hover:shadow-md transition-all">
                      Gaming Headphones
                    </button>
                  </div>
                </div>
              </div>
            )}            {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.is_bot ? 'justify-start' : 'justify-end'} animate-message-slide`}
            style={{ animationDelay: `${idx * 0.1}s` }}
          >
            <div className={`max-w-[85%] ${msg.is_bot ? 'mr-auto' : 'ml-auto'}`}>
              {/* Enhanced Message Bubble */}              <div
                className={`${msg.is_bot ? 'message-bot' : 'message-user'} ${idx === 0 && msg.is_bot ? 'first-bot-message' : ''} message-bubble rounded-2xl px-5 py-4 shadow-lg backdrop-blur-sm border transition-all duration-300 hover:shadow-xl`}
              >{msg.is_bot && (
                  <div className="flex items-center mb-3">
                    <div className="w-7 h-7 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mr-3 shadow-md">
                      <span className="text-xs text-white font-bold">A</span>
                    </div>
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-sm font-semibold text-gray-800">Alex - NexTechAI</span>
                      <span className="bot-badge">AI Assistant</span>
                      <div className="flex items-center text-xs text-green-600 bg-green-50 px-2 py-0.5 rounded-full border border-green-200">
                        <div className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1 animate-pulse"></div>
                        <span>Online</span>
                      </div>
                      {idx === 0 && (
                        <div className="text-xs text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full border border-blue-200">
                          <span className="flex items-center"><SparklesIcon className="w-3 h-3 mr-1" />AI Recommendations</span>
                        </div>
                      )}
                      {msg.conversation_type && (
                        <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                          msg.conversation_type === 'product_recommendation' ? 'bg-green-100 text-green-700 border border-green-200' :
                          msg.conversation_type === 'greeting' ? 'bg-blue-100 text-blue-700 border border-blue-200' :
                          msg.conversation_type === 'clarification' ? 'bg-yellow-100 text-yellow-700 border border-yellow-200' :
                          'bg-gray-100 text-gray-700 border border-gray-200'
                        }`}>
                          {msg.conversation_type.replace('_', ' ')}
                        </span>
                      )}
                    </div>
                  </div>
                )}
                  {idx === 0 && msg.is_bot ? (
                  <>
                    {/* Assistant info banner for first message */}
                    <div className="mb-4 px-4 py-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center">
                          <div className="w-9 h-9 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mr-3 shadow-md">
                            <SparklesIcon className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <h3 className="font-medium text-gray-900">Alex - NexTechAI Assistant</h3>
                            <p className="text-xs text-blue-600">AI-Powered Electronics Shopping Expert</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="text-xs px-2 py-1 bg-green-50 text-green-600 rounded-full border border-green-100 flex items-center">
                            <div className="w-1.5 h-1.5 mr-1 bg-green-500 rounded-full animate-pulse"></div>
                            Online
                          </div>
                          <div className="text-xs px-2 py-1 bg-blue-50 text-blue-600 rounded-full border border-blue-100 flex items-center">
                            <SparklesIcon className="w-3 h-3 mr-1" />
                            AI Recommendations
                          </div>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-2 mt-2">
                        <span className="text-xs px-2 py-0.5 bg-purple-50 text-purple-600 rounded-full border border-purple-100">💡 Smart Shopping</span>
                        <span className="text-xs px-2 py-0.5 bg-green-50 text-green-600 rounded-full border border-green-100">📱 Tech Products</span>
                        <span className="text-xs px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full border border-blue-100">🔍 Personalized Search</span>
                      </div>
                    </div>
                    <p className="whitespace-pre-wrap leading-relaxed text-[15px]">{msg.message}</p>
                  </>
                ) : (
                  <p className="whitespace-pre-wrap leading-relaxed text-[15px]">{msg.message}</p>
                )}
                
                {/* Enhanced product count display */}
                {msg.is_bot && msg.total_found > 0 && (
                  <div className="mt-3 p-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200/50">
                    <div className="flex items-center text-sm font-medium text-blue-700">
                      <SparklesIcon className="w-4 h-4 mr-2" />
                      Found {msg.total_found} product{msg.total_found !== 1 ? 's' : ''} matching your criteria
                    </div>
                  </div>
                )}
                  <div className="flex justify-between items-center mt-3">
                  <span className={`message-timestamp ${msg.is_bot ? 'text-gray-500' : 'text-blue-100'}`}>
                    {format(new Date(msg.created_at), 'HH:mm')}
                  </span>
                  {!msg.is_bot && (
                    <div className="flex items-center text-blue-100 text-xs">
                      <div className="w-2 h-2 bg-blue-200 rounded-full mr-1"></div>
                      Sent
                    </div>
                  )}
                </div>
              </div>              {/* Enhanced Products Grid */}
              {msg.is_bot && msg.products && msg.products.length > 0 && (
                <div className="products-recommendation mt-6">                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center">
                      <SparklesIcon className="w-3 h-3 mr-1 text-blue-500" />
                      <span className="text-xs font-semibold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                        Recommended Products
                      </span>
                    </div>
                    <div className="text-[10px] text-white bg-gradient-to-r from-blue-500 to-purple-600 px-1.5 py-0.5 rounded-full shadow-sm">
                      {msg.products.length} item{msg.products.length !== 1 ? 's' : ''}
                    </div>
                  </div><div className="products-grid p-2 bg-gradient-to-r from-gray-50 to-blue-50 rounded-lg border border-gray-200/50 shadow-inner">
                    {msg.products.map((product) => (
                      <div key={product.id} className="product-card">
                        <ProductCard product={product} />
                      </div>
                    ))}
                  </div>
                </div>
              )}              {/* Enhanced Smart Suggestions - Compact Design */}              {msg.is_bot && (idx === messages.length - 1 || idx === 0) && !loading && suggestions.length > 0 && (
                <div className="mt-3 animate-fade-in">
                  <div className="flex items-center mb-1">
                    <LightBulbIcon className="w-3 h-3 mr-1 text-amber-500" />
                    <span className="text-xs font-medium text-gray-700">
                      Smart Suggestions
                    </span>
                    <div className="text-[10px] text-amber-600 bg-amber-50 px-1.5 py-0.5 rounded-full border border-amber-200 ml-1">
                      AI
                    </div>
                  </div>
                  <div className="suggestions-grid grid gap-1.5 grid-cols-1 md:grid-cols-2">
                    {suggestions.map((suggestion, suggestionIdx) => (                      <button
                        key={suggestionIdx}
                        onClick={() => handleSuggestionClick(suggestion)}
                        className="suggestion-chip group bg-white hover:bg-blue-50 px-2.5 py-1.5 rounded-md border border-gray-200 hover:border-blue-300 text-left text-xs transition-all duration-200 flex items-center justify-between animate-suggestion-reveal shadow-sm hover:shadow"
                        style={{ animationDelay: `${suggestionIdx * 0.05}s` }}
                      >
                        <span className="text-gray-700 font-medium truncate">
                          {suggestion}
                        </span>
                        <ArrowRightIcon className="w-2.5 h-2.5 text-blue-400 opacity-0 group-hover:opacity-100 transition-all duration-300 ml-1 flex-shrink-0" />
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}        {loading && (
          <div className="flex justify-start animate-fade-in">
            <div className="max-w-[85%] mr-auto">
              <div className="chat-typing-indicator shadow-lg rounded-2xl px-5 py-4 backdrop-blur-sm">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-7 h-7 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-md">
                    <span className="text-xs text-white font-bold">A</span>
                  </div>
                  <span className="text-sm font-semibold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Alex is thinking...</span>
                  <div className="flex items-center space-x-1">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <SparklesIcon className="w-4 h-4 animate-spin text-blue-500" />
                  <span>Analyzing your request and finding the best products...</span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} className="h-4" />
        <div ref={messagesEndRef} />
      </div>      {/* Enhanced Conversation Starters */}
      {messages.length === 1 && suggestions.length === 0 && (
        <div className="px-6 pb-6">
          <div className="text-center mb-6">
            <div className="text-lg font-semibold text-gray-800 mb-2">Ready to find your perfect tech?</div>
            <div className="text-sm text-gray-600 flex items-center justify-center">
              <MagnifyingGlassIcon className="w-4 h-4 mr-1" />
              Try one of these popular searches to get started:
            </div>
          </div>
          <div className="suggestions-container">
            {conversationStarters.map((starter, idx) => (
              <button
                key={idx}
                onClick={() => handleStarterClick(starter)}
                className="suggestion-item group flex items-center justify-between p-5 text-left relative overflow-hidden"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="relative z-10 flex-1">
                  <span className="text-sm font-medium block mb-1">
                    {starter}
                  </span>
                  <span className="text-xs text-gray-500">
                    Click to start conversation
                  </span>
                </div>
                <ArrowRightIcon className="w-5 h-5 text-gray-300 opacity-0 transition-all duration-300 transform group-hover:translate-x-1 relative z-10" />
              </button>
            ))}
          </div>
        </div>
      )}      {/* Enhanced Quick Actions Bar */}
      {!loading && messages.length > 1 && (
        <div className="px-6 pb-4">
          <div className="text-center mb-3">
            <span className="text-xs text-gray-500 font-medium">Quick Actions</span>
          </div>
          <div className="flex flex-wrap gap-3 justify-center">
            <button
              onClick={() => handleSuggestionClick("Show me trending smartphones and laptops")}
              className="suggestion-item px-4 py-2 text-sm bg-gradient-to-r from-green-50 to-emerald-50 text-green-700 border border-green-200 rounded-xl"
            >
              <span className="flex items-center">
                🔥 <span className="ml-1 font-medium">Trending</span>
              </span>
            </button>
            <button
              onClick={() => handleSuggestionClick("Show me discounted electronics under $500")}
              className="suggestion-item px-4 py-2 text-sm bg-gradient-to-r from-red-50 to-pink-50 text-red-700 border border-red-200 rounded-xl"
            >
              <span className="flex items-center">
                💰 <span className="ml-1 font-medium">Deals</span>
              </span>
            </button>
            <button
              onClick={() => handleSuggestionClick("Show me premium electronics above $800")}
              className="suggestion-item px-4 py-2 text-sm bg-gradient-to-r from-purple-50 to-indigo-50 text-purple-700 border border-purple-200 rounded-xl"
            >
              <span className="flex items-center">
                ⭐ <span className="ml-1 font-medium">Premium</span>
              </span>
            </button>
            <button
              onClick={() => handleSuggestionClick("Show me budget electronics under $200")}
              className="suggestion-item px-4 py-2 text-sm bg-gradient-to-r from-blue-50 to-cyan-50 text-blue-700 border border-blue-200 rounded-xl"
            >
              <span className="flex items-center">
                💡 <span className="ml-1 font-medium">Budget</span>
              </span>
            </button>
          </div>
        </div>
      )}{/* Enhanced Chat Input */}      <div className="chat-input-container sticky bottom-0 bg-white border-t border-gray-200/50 px-4 py-3 backdrop-blur-sm z-10 w-full">
        {/* Enhanced input suggestions preview - completely removed to avoid duplication */}
          <form onSubmit={handleSubmit} className="flex space-x-4">
          <div className="flex-1 relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask Alex about premium electronics, trending tech, or specific products..."
              className="chat-input w-full px-10 py-4 border-2 border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 hover:bg-white transition-all duration-200 text-sm font-medium pr-12"
              disabled={loading}
              autoFocus
            />
            <div className="absolute left-3 top-1/2 transform -translate-y-1/2">
              <SparklesIcon className="w-4 h-4 text-blue-400" />
            </div>
            {input && (
              <button
                type="button"
                onClick={() => setInput('')}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
              >
                <span className="text-lg">✕</span>
              </button>
            )}
          </div>
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="chat-send-button px-8 py-4 rounded-2xl transition-all duration-200 transform hover:scale-105 disabled:transform-none"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <span className="flex items-center">
                Send
                <ArrowRightIcon className="w-4 h-4 ml-2" />
              </span>
            )}
          </button>        </form>
      </div>
        </div>
      </div>
    </div>
  );
}