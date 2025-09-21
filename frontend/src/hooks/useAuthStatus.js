// src/hooks/useAuthStatus.js

import { useState, useEffect } from 'react';

/**
 * A custom hook to check the user's authentication and role status.
 * This hook is useful for rendering different content or redirecting users
 * based on their logged-in status and privileges.
 * @returns {object} An object containing isAuthenticated and isAdmin boolean values.
 */
const useAuthStatus = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  
  useEffect(() => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    
    // Check if a token exists
    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }

    // Check if the user is an admin
    if (role === 'admin') {
      setIsAdmin(true);
    } else {
      setIsAdmin(false);
    }
    
  }, []); // The empty dependency array ensures this runs only once on mount

  return { isAuthenticated, isAdmin };
};

export default useAuthStatus;