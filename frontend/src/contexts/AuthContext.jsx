import React, { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import api from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const checkAndRefreshToken = async () => {
      const token = localStorage.getItem('access_token');
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const decoded = jwtDecode(token);
        
        // If token is expired but we have a refresh token, try to refresh
        if (decoded.exp * 1000 <= Date.now() && refreshToken) {
          try {
            const response = await api.post('/auth/refresh', {}, {
              headers: { Authorization: `Bearer ${refreshToken}` }
            });
            const { access_token } = response.data;
            
            localStorage.setItem('access_token', access_token);
            api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
            
            const newDecoded = jwtDecode(access_token);
            setUser(newDecoded);
          } catch (refreshError) {
            console.error('Error refreshing token:', refreshError);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            setUser(null);
          }
        } else if (decoded.exp * 1000 > Date.now()) {
          // Token is still valid
          setUser(decoded);
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        } else {
          // Token is expired and no refresh token
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          setUser(null);
        }
      } catch (error) {
        console.error('Error decoding token:', error);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
      }
      setLoading(false);
    };

    checkAndRefreshToken();
  }, []);const login = async (username, password) => {
    try {
      const response = await api.post('/auth/login', { username, password });
      const { access_token, refresh_token, user } = response.data;
      
      if (!access_token || !refresh_token) {
        throw new Error('Invalid response from server');
      }
      
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Set the user state
      const decoded = jwtDecode(access_token);
      setUser(decoded);
      
      // Clear any cached cart data from previous user
      localStorage.removeItem('cart_cache');
      
      setUser(user);
      return user;
    } catch (error) {
      throw error.response?.data?.error || 'Login failed';
    }
  };

  const register = async (username, email, password) => {
    try {
      const response = await api.post('/auth/register', {
        username,
        email,
        password,
      });
      const { access_token, refresh_token, user } = response.data;
      
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      setUser(user);
      return user;
    } catch (error) {
      throw error.response?.data?.error || 'Registration failed';
    }
  };
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('cart_cache'); // Clear cart cache on logout
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
  };

  const refreshToken = async () => {
    try {
      const refresh_token = localStorage.getItem('refresh_token');
      if (!refresh_token) throw new Error('No refresh token');

      const response = await api.post('/auth/refresh', {}, {
        headers: { Authorization: `Bearer ${refresh_token}` }
      });
      
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      return access_token;
    } catch (error) {
      logout();
      throw error;
    }
  };

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    refreshToken,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};