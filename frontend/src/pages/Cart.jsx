import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import api from '../services/api';
import CheckoutForm from '../components/CheckoutForm';

export default function Cart() {
  const [cart, setCart] = useState({ items: [] });
  const [loading, setLoading] = useState(true);
  const [showCheckout, setShowCheckout] = useState(false);
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCart();
  }, []);
  const fetchCart = async () => {
    try {
      const response = await api.get('/cart');
      setCart(response.data.cart || { items: [] });
      setLoading(false);
    } catch (error) {
      console.error('Error fetching cart:', error);
      setCart({ items: [] });
      setLoading(false);
    }
  };

  const updateQuantity = async (itemId, quantity) => {
    try {
      await api.put(`/cart/items/${itemId}`, { quantity });
      fetchCart();
    } catch (error) {
      console.error('Error updating quantity:', error);
    }
  };

  const removeItem = async (itemId) => {
    try {
      await api.delete(`/cart/items/${itemId}`);
      fetchCart();
    } catch (error) {
      console.error('Error removing item:', error);
    }
  };  const handleCheckout = async (orderData) => {
    setCheckoutLoading(true);
    try {
      const response = await api.post('/orders', orderData);
      toast.success('Order placed successfully!');
      // Navigate to orders page to see all orders
      navigate('/orders');
    } catch (error) {
      console.error('Error during checkout:', error);
      toast.error('Failed to place order. Please try again.');
    } finally {
      setCheckoutLoading(false);
    }
  };

  const handleCancelCheckout = () => {
    setShowCheckout(false);
  };
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }
  // Render checkout form as modal overlay

  const total = cart.items?.reduce((sum, item) => sum + item.product.price * item.quantity, 0) || 0;

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">Your Cart</h2>
      {(!cart.items || cart.items.length === 0) ? (
        <div className="text-center py-8">
          <p className="text-gray-600 mb-4">Your cart is empty</p>
          <button
            onClick={() => navigate('/products')}
            className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition-colors"
          >
            Continue Shopping
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {cart.items?.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between border rounded-lg p-4 bg-white"
            >
              <div className="flex items-center space-x-4">
                <img
                  src={item.product.image_url}
                  alt={item.product.name}
                  className="w-20 h-20 object-cover rounded"
                />
                <div>
                  <h3 className="font-medium">{item.product.name}</h3>
                  <p className="text-gray-600">${item.product.price.toFixed(2)}</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center border rounded">
                  <button
                    onClick={() => updateQuantity(item.id, Math.max(0, item.quantity - 1))}
                    className="px-3 py-1 hover:bg-gray-100"
                  >
                    -
                  </button>
                  <span className="px-3 py-1 border-x">{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    className="px-3 py-1 hover:bg-gray-100"
                  >
                    +
                  </button>
                </div>
                <button
                  onClick={() => removeItem(item.id)}
                  className="text-red-500 hover:text-red-700"
                >
                  Remove
                </button>
              </div>
            </div>
          ))}

          <div className="mt-8 bg-white rounded-lg p-6 shadow-sm">
            <div className="flex justify-between mb-4">
              <span className="text-lg font-medium">Total:</span>
              <span className="text-lg font-bold">${total.toFixed(2)}</span>
            </div>            <button
              onClick={() => setShowCheckout(true)}
              className="w-full bg-primary-600 text-white py-3 rounded-lg hover:bg-primary-700 transition-colors"
            >
              Proceed to Checkout
            </button>          </div>
        </div>
      )}
      
      {/* Checkout Modal */}
      {showCheckout && (
        <CheckoutForm 
          cart={cart}
          onSubmit={handleCheckout}
          onCancel={handleCancelCheckout}
          loading={checkoutLoading}
        />
      )}
    </div>
  );
}
