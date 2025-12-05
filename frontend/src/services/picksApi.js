// src/services/picksApi.js
import axios from 'axios';
import { getAuth } from 'firebase/auth';

const API_BASE_URL = 'http://localhost:8000/api';

// Helper to get Firebase auth token with better error handling
const getAuthToken = async () => {
  const auth = getAuth();
  
  // Wait for auth to be ready (max 3 seconds)
  let attempts = 0;
  while (!auth.currentUser && attempts < 30) {
    await new Promise(resolve => setTimeout(resolve, 100));
    attempts++;
  }
  
  const user = auth.currentUser;
  
  if (!user) {
    console.warn('No authenticated user found');
    return null; // Return null instead of throwing
  }
  
  try {
    return await user.getIdToken();
  } catch (error) {
    console.error('Error getting ID token:', error);
    return null;
  }
};

// Helper to get headers with auth token (optional)
const getAuthHeaders = async () => {
  const token = await getAuthToken();
  if (token) {
    return {
      'Authorization': `Bearer ${token}`
    };
  }
  return {}; // Return empty headers if no token
};

export const savePick = async (pickData) => {
  try {
    const headers = await getAuthHeaders();
    const response = await axios.post(`${API_BASE_URL}/picks/`, pickData, { headers });
    return response.data;
  } catch (error) {
    console.error('Error saving pick:', error);
    throw error;
  }
};

export const deletePick = async (pickData) => {
  try {
    const headers = await getAuthHeaders();
    const response = await axios.delete(`${API_BASE_URL}/picks/`, { 
      headers,
      data: pickData 
    });
    return response.data;
  } catch (error) {
    console.error('Error deleting pick:', error);
    throw error;
  }
};

export const getActivePicks = async () => {
  try {
    const headers = await getAuthHeaders();
    const response = await axios.get(`${API_BASE_URL}/picks/active`, { headers });
    return response.data.picks || [];
  } catch (error) {
    console.error('Error fetching active picks:', error);
    return [];
  }
};

export const checkUserPicks = async (gameId) => {
  try {
    const headers = await getAuthHeaders();
    const response = await axios.get(`${API_BASE_URL}/picks/check/${gameId}`, { headers });
    return response.data;
  } catch (error) {
    console.error('Error checking user picks:', error);
    return { picks: {} };
  }
};

export const getPickHistory = async (filters = {}) => {
  try {
    const headers = await getAuthHeaders();
    const response = await axios.get(`${API_BASE_URL}/picks/history`, { 
      headers,
      params: filters 
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching pick history:', error);
    return [];
  }
};

export const getUserStats = async () => {
  try {
    const headers = await getAuthHeaders();
    const response = await axios.get(`${API_BASE_URL}/picks/stats`, { headers });
    return response.data;
  } catch (error) {
    console.error('Error fetching user stats:', error);
    throw error;
  }
};

export const getLeaderboard = async (timeframe = 'overall') => {
  try {
    const userId = 1; // Test user for now
    
    const response = await axios.get(`${API_BASE_URL}/grading/leaderboard`, {
      params: {
        timeframe: timeframe,
        current_user_id: userId
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error fetching leaderboard:', error);
    throw error;
  }
};