// src/api/auth.js

import axios from 'axios';

// The base URL for your Django backend
export const API_URL = 'http://127.0.0.1:8000/api/v1/';

// Create an Axios instance with the base URL
const api = axios.create({
  baseURL: API_URL,
});

/**
 * Logs in a user by sending credentials to the backend.
 * Upon success, stores the token and role in localStorage and sets the Authorization header.
 * @param {string} email - The user's email address.
 * @param {string} password - The user's password.
 * @returns {Promise<object>} The response data from the backend, including token and role.
 */
export const login = async (email, password) => {
  const response = await api.post('auth/login/', { email, password });
  
  // Store the token and role from the response
  localStorage.setItem('token', response.data.token);
  localStorage.setItem('role', response.data.role);

  // Set the default Authorization header for all future requests
  axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`;
  
  return response.data;
};

/**
 * Logs the user out by clearing the token and role from local storage and removing the Authorization header.
 */
export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  delete axios.defaults.headers.common['Authorization'];
  window.location.href = '/login';
};

// Immediately set the Authorization header on app load if a token exists in localStorage
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Token ${token}`;
}

export default api;