// src/api/employees.js

import api from './auth';

/**
 * A helper function to get the authentication headers.
 * This ensures that every request to a protected endpoint includes the user's token.
 * @returns {object} The headers object with the Authorization token.
 */
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error("No authentication token found. Please log in.");
  }
  return {
    headers: {
      Authorization: `Token ${token}`,
    },
  };
};

/**
 * Fetches a list of all employees from the backend.
 * This is typically an admin-only endpoint.
 * @returns {Promise<Array>} A list of employee objects.
 */
export const getEmployees = async () => {
  try {
    // First, try to get the count of total employees
    const response = await api.get('employees/employees/?page_size=100', getAuthHeaders());
    
    // Handle paginated response - return just the results array
    if (response.data && typeof response.data === 'object' && 'results' in response.data) {
      let allEmployees = response.data.results;
      
      // If there are more pages, fetch them all
      if (response.data.next) {
        let nextUrl = response.data.next;
        while (nextUrl) {
          const nextResponse = await api.get(nextUrl.replace(api.defaults.baseURL, ''), getAuthHeaders());
          allEmployees = [...allEmployees, ...nextResponse.data.results];
          nextUrl = nextResponse.data.next;
        }
      }
      
      return allEmployees;
    }
    // Fallback for non-paginated response
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error fetching employees:', error);
    throw error;
  }
};

/**
 * Fetches the current user's employee profile.
 * @returns {Promise<object>} The current user's employee object.
 */
export const getMyProfile = async () => {
  try {
    const response = await api.get('employees/employees/me/', getAuthHeaders());
    return response.data;
  } catch (error) {
    console.error('Error fetching my profile:', error);
    throw error;
  }
};

/**
 * Fetches a single employee's details by their ID.
 * @param {number} employeeId - The ID of the employee to fetch.
 * @returns {Promise<object>} The employee object.
 */
export const getEmployee = async (employeeId) => {
  try {
    const response = await api.get(`employees/employees/${employeeId}/`, getAuthHeaders());
    return response.data;
  } catch (error) {
    console.error(`Error fetching employee with ID ${employeeId}:`, error);
    throw error;
  }
};

/**
 * Creates a new employee by sending a POST request to the backend.
 * @param {object} employeeData - The data for the new employee.
 * @returns {Promise<object>} The newly created employee object.
 */
export const createEmployee = async (employeeData) => {
  try {
    const response = await api.post('employees/employees/', employeeData, getAuthHeaders());
    return response.data;
  } catch (error) {
    console.error('Error creating new employee:', error);
    throw error;
  }
};

/**
 * Updates an existing employee by their ID.
 * @param {number} employeeId - The ID of the employee to update.
 * @param {object} employeeData - The updated data for the employee.
 * @returns {Promise<object>} The updated employee object.
 */
export const updateEmployee = async (employeeId, employeeData) => {
  try {
    const response = await api.put(`employees/employees/${employeeId}/`, employeeData, getAuthHeaders());
    return response.data;
  } catch (error) {
    console.error(`Error updating employee with ID ${employeeId}:`, error);
    throw error;
  }
};

/**
 * Deletes an employee by their ID.
 * @param {number} employeeId - The ID of the employee to delete.
 * @returns {Promise<void>}
 */
export const deleteEmployee = async (employeeId) => {
  try {
    await api.delete(`employees/employees/${employeeId}/`, getAuthHeaders());
  } catch (error) {
    console.error(`Error deleting employee with ID ${employeeId}:`, error);
    throw error;
  }
};