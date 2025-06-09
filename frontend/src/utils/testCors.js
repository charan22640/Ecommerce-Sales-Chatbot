import api from '../services/api';

export const testCorsConnection = async () => {
  try {
    const response = await api.get('/auth/test-cors', { 
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      }
    });
    console.log('CORS test successful:', response.data);
    return { success: true, data: response.data };
  } catch (error) {
    console.error('CORS test failed:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      headers: error.response?.headers
    });
    return { success: false, error };
  }
};
