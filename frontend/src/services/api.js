import axios from 'axios';

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true, // Enable credentials for both development and production
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else if (!config.url.includes('/auth/login') && !config.url.includes('/auth/register')) {
      // Redirect to login if no token and trying to access protected route
      window.location.href = '/login';
      return Promise.reject('No auth token');
    }
    // Don't modify Content-Type for FormData (multipart/form-data)
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Log error details in production
    if (import.meta.env.PROD) {
      console.error('API Error:', {
        url: error.config?.url,
        method: error.config?.method,
        status: error.response?.status,
        message: error.message,
        timestamp: new Date().toISOString()
      });
    }

    // Don't retry if it's already a refresh token request or we don't have a refresh token
    if (originalRequest.url === '/auth/refresh' || !localStorage.getItem('refresh_token')) {
      return Promise.reject(error);
    }

    // Handle 401 errors with token refresh
    if (error.response?.status === 401 && !originalRequest._retry && !isRefreshing) {
      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const refresh_token = localStorage.getItem('refresh_token');
        if (!refresh_token) throw new Error('No refresh token');

        const response = await axios.post(
          `${api.defaults.baseURL}/auth/refresh`,
          {},
          {
            headers: { Authorization: `Bearer ${refresh_token}` }
          }
        );

        const { access_token } = response.data;
        
        if (!access_token) {
          throw new Error('No access token received');
        }

        localStorage.setItem('access_token', access_token);
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        originalRequest.headers.Authorization = `Bearer ${access_token}`;

        // Process any queued requests
        processQueue(null, access_token);
        
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('cart_cache');
        
        // Only redirect for auth errors if not already on auth pages
        if (!originalRequest.url.includes('auth')) {
          window.location.href = `/login?error=${encodeURIComponent(refreshError.message)}&redirect=${encodeURIComponent(window.location.pathname)}`;
        }
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    // Handle other error cases
    if (error.response?.status === 403) {
      // Handle forbidden errors
      console.error('Access forbidden:', error.response.data);
    } else if (error.response?.status === 500) {
      // Handle server errors
      console.error('Server error:', error.response.data);
    }

    return Promise.reject(error);
  }
);

// Cart endpoints
const cartApi = {
  getCart: () => api.get('/cart'),
  addToCart: (productId, quantity = 1) => api.post('/cart/items', { product_id: productId, quantity }),
  updateCartItem: (itemId, quantity) => api.put(`/cart/items/${itemId}`, { quantity }),
  removeCartItem: (itemId) => api.delete(`/cart/items/${itemId}`),
  clearCart: () => api.delete('/cart')
};

// Order endpoints
const orderApi = {
  getOrders: () => api.get('/orders'),
  getOrder: (orderId) => api.get(`/orders/${orderId}`),
  createOrder: () => api.post('/orders'),
  cancelOrder: (orderId) => api.delete(`/orders/${orderId}`)
};

export const { getCart, addToCart, updateCartItem, removeCartItem, clearCart } = cartApi;
export const { getOrders, getOrder, createOrder, cancelOrder } = orderApi;

export default api;