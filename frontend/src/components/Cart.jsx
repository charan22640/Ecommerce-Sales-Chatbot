import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

const Cart = () => {
  const [cart, setCart] = useState({ items: [] });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { user } = useAuth();
  
  useEffect(() => {
    if (user) {
      const initializeCart = async () => {
        // Clear any stale cart state when user changes
        setCart({ items: [] });
        setLoading(true);
        
        await cleanupCart(); // Clean up stale items first
        await fetchCart(); // Then fetch the clean cart
      };
      initializeCart();
    } else {
      // Clear cart when no user is logged in
      setCart({ items: [] });
      setLoading(false);
    }
  }, [user]); // Add user dependency to reinitialize when user changes
  const fetchCart = async () => {
    try {
      const response = await api.get('/cart');
      setCart(response.data.cart || { items: [] });
      setLoading(false);
    } catch (error) {
      console.error('Error fetching cart:', error);
      // If there's an authentication error, the cart might be invalid
      if (error.response?.status === 401) {
        setCart({ items: [] });
      }
      setLoading(false);
    }
  };

  const cleanupCart = async () => {
    try {
      await api.post('/cart/cleanup');
      fetchCart(); // Refresh cart after cleanup
    } catch (error) {
      console.error('Error cleaning up cart:', error);
    }
  };  const updateQuantity = async (itemId, quantity) => {
    try {
      if (quantity <= 0) {
        await removeItem(itemId);
        return;
      }
      await api.put(`/cart/items/${itemId}`, { quantity });
      await fetchCart(); // Refresh cart after update
    } catch (error) {
      console.error('Error updating quantity:', error);
      // Handle 404 errors (item doesn't exist or doesn't belong to current user)
      if (error.response?.status === 404) {
        console.log('Cart item not found, refreshing cart to sync state...');
        await fetchCart(); // Refresh cart to get current state
        alert('Cart item not found. Your cart has been refreshed.');
      } else if (error.response?.data?.error) {
        alert(`Error: ${error.response.data.error}`);
      } else {
        alert('Failed to update quantity. Please try again.');
      }
    }
  };

  const removeItem = async (itemId) => {
    try {
      await api.delete(`/cart/items/${itemId}`);
      await fetchCart(); // Refresh cart after removal
    } catch (error) {
      console.error('Error removing item:', error);
      // Handle 404 errors (item doesn't exist or doesn't belong to current user)
      if (error.response?.status === 404) {
        console.log('Cart item not found, refreshing cart to sync state...');
        await fetchCart(); // Refresh cart to get current state
        alert('Cart item not found. Your cart has been refreshed.');
      } else if (error.response?.data?.error) {
        alert(`Error: ${error.response.data.error}`);
      } else {
        alert('Failed to remove item. Please try again.');
      }
    }
  };

  const checkout = async () => {
    try {
      const response = await api.post('/orders');
      navigate(`/orders/${response.data.id}`);
    } catch (error) {
      console.error('Error during checkout:', error);
    }
  };

  if (loading) {
    return <div className="text-center p-4">Loading...</div>;
  }

  const total = cart.items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">Your Cart</h2>
      {cart.items.length === 0 ? (
        <div className="text-center py-8">
          <p>Your cart is empty</p>
          <button
            onClick={() => navigate('/products')}
            className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Continue Shopping
          </button>
        </div>
      ) : (
        <>
          <div className="space-y-4">
            {cart.items.map((item) => (
              <div key={item.id} className="flex items-center border p-4 rounded">
                <img
                  src={item.product.image_url}
                  alt={item.product.name}
                  className="w-20 h-20 object-cover rounded"
                />
                <div className="flex-1 ml-4">
                  <h3 className="font-semibold">{item.product.name}</h3>
                  <p className="text-gray-600">${item.product.price}</p>
                </div>
                <div className="flex items-center space-x-2">                  <button
                    onClick={() => {
                      const newQuantity = Math.max(1, item.quantity - 1);
                      if (newQuantity === 1 && item.quantity === 1) {
                        removeItem(item.id);
                      } else {
                        updateQuantity(item.id, newQuantity);
                      }
                    }}
                    className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300 transition-colors"
                  >
                    -
                  </button>
                  <span>{item.quantity}</span>                  <button
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300 transition-colors"
                  >
                    +
                  </button>
                  <button
                    onClick={() => removeItem(item.id)}
                    className="ml-4 text-red-500 hover:text-red-700"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-8 border-t pt-4">
            <div className="flex justify-between items-center mb-4">
              <span className="text-xl font-semibold">Total:</span>
              <span className="text-xl">${total.toFixed(2)}</span>
            </div>
            <button
              onClick={checkout}
              className="w-full bg-green-500 text-white py-3 rounded-lg hover:bg-green-600"
            >
              Proceed to Checkout
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Cart;
