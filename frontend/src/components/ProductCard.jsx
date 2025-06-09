import React, { useState } from 'react';
import { StarIcon } from '@heroicons/react/20/solid';
import { toast } from 'react-toastify';
import api from '../services/api';

export default function ProductCard({ product }) {
  const [loading, setLoading] = useState(false);
  const addToCart = async () => {
    if (product.stock_quantity === 0) {
      toast.error('This item is out of stock');
      return;
    }

    setLoading(true);
    try {
      await api.post('/cart/items', {
        product_id: product.id,
        quantity: 1
      });
      toast.success('Added to cart successfully!');
    } catch (error) {
      console.error('Error adding to cart:', error);
      toast.error(error.response?.data?.message || 'Failed to add item to cart');
    } finally {
      setLoading(false);
    }
  };  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden h-full flex flex-col">
      {/* Product Image */}
      <div className="relative aspect-[4/3] w-full overflow-hidden bg-gray-200">
        <img
          src={product.image_url.startsWith('http') 
            ? product.image_url 
            : `${import.meta.env.VITE_API_URL}/products/${product.image_url}`}
          alt={product.name}
          className="absolute inset-0 h-full w-full object-cover object-center"
          onError={(e) => {
            e.target.src = `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(
              `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
                <rect width="300" height="300" fill="#f3f4f6"/>
                <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="system-ui" font-size="16" fill="#9ca3af">
                  No Image Available
                </text>
              </svg>`
            )}`;
          }}
        />
      </div>

      {/* Product Info */}
      <div className="p-3 flex-1 flex flex-col">
        <h3 className="text-xs font-medium text-gray-900 line-clamp-1">{product.name}</h3>
        
        {/* Price */}
        <p className="mt-1 text-base font-bold text-gray-900">
          ${product.price.toFixed(2)}
        </p>

        {/* Rating */}
        <div className="mt-1 flex items-center">
          {[0, 1, 2, 3, 4].map((rating) => (
            <StarIcon
              key={rating}
              className={`h-3 w-3 flex-shrink-0 ${
                product.rating > rating ? 'text-yellow-400' : 'text-gray-200'
              }`}
              aria-hidden="true"
            />
          ))}
          <span className="ml-1 text-xs text-gray-500">
            ({product.rating.toFixed(1)})
          </span>
        </div>

        {/* Condensed Info */}
        <div className="mt-1 text-xs text-gray-500 line-clamp-1">
          {product.category}{product.subcategory ? ` - ${product.subcategory}` : ''}
          {product.color ? ` • ${product.color}` : ''}
        </div>

        {/* Stock Status */}
        <div className="mt-1 text-xs">
          {product.stock_quantity > 0 ? (
            <span className="text-green-600 font-medium">{product.stock_quantity} in stock</span>
          ) : (
            <span className="text-red-600 font-medium">Out of stock</span>
          )}
        </div>

        {/* Add to Cart Button - placed at bottom */}
        <button
          onClick={addToCart}
          disabled={loading || product.stock_quantity === 0}
          className={`mt-2 w-full rounded-md px-2 py-1.5 text-xs font-semibold text-white shadow-sm transition-colors
            ${loading 
              ? 'bg-gray-400 cursor-not-allowed'
              : product.stock_quantity === 0
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-primary-600 hover:bg-primary-700 active:bg-primary-800 focus:outline-none focus:ring-1 focus:ring-primary-500 focus:ring-offset-1'
            }`}
        >
          {loading ? 'Adding...' : product.stock_quantity === 0 ? 'Out of Stock' : 'Add to Cart'}
        </button>
      </div>
    </div>
  );
}