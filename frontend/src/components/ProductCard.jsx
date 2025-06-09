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
  };
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden h-full flex flex-col">
      {/* Product Image */}
      <div className="relative aspect-square w-full overflow-hidden bg-gray-200">
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
      <div className="p-4 flex-1 flex flex-col">
        <h3 className="text-sm font-medium text-gray-900 line-clamp-2">{product.name}</h3>
        
        {/* Price */}
        <p className="mt-2 text-lg font-bold text-gray-900">
          ${product.price.toFixed(2)}
        </p>

        {/* Categories */}
        {product.subcategory && (
          <div className="mt-1 text-sm text-gray-500">
            {product.category} - {product.subcategory}
          </div>
        )}

        {/* Rating */}
        <div className="mt-2 flex items-center">
          {[0, 1, 2, 3, 4].map((rating) => (
            <StarIcon
              key={rating}
              className={`h-4 w-4 flex-shrink-0 ${
                product.rating > rating ? 'text-yellow-400' : 'text-gray-200'
              }`}
              aria-hidden="true"
            />
          ))}
          <span className="ml-1 text-sm text-gray-500">
            ({product.rating.toFixed(1)})
          </span>
        </div>

        {/* Additional Info Tags */}
        <div className="mt-3 flex flex-wrap gap-1">
          <span className="inline-flex items-center rounded-full bg-primary-50 px-2 py-1 text-xs font-medium text-primary-700">
            {product.category}
          </span>
          {product.style && (
            <span className="inline-flex items-center rounded-full bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600">
              {product.style}
            </span>
          )}
          {product.color && (
            <span className="inline-flex items-center rounded-full bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600">
              {product.color}
            </span>
          )}
        </div>

        {/* Stock Status */}
        <div className="mt-3 text-sm">
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
          className={`mt-4 w-full rounded-md px-3 py-2 text-sm font-semibold text-white shadow-sm transition-colors
            ${loading 
              ? 'bg-gray-400 cursor-not-allowed'
              : product.stock_quantity === 0
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-primary-600 hover:bg-primary-700 active:bg-primary-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2'
            }`}
        >
          {loading ? 'Adding...' : product.stock_quantity === 0 ? 'Out of Stock' : 'Add to Cart'}
        </button>
      </div>
    </div>
  );
}