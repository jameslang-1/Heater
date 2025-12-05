// src/services/picksApi.js
import axios from 'axios';
import { getAuth } from 'firebase/auth';

const API_BASE_URL = 'http://localhost:8000/api';

// Helper to get Firebase auth token
const getAuthToken = async () => {
  const auth = getAuth();
  const user = auth.currentUser;
  
  if (!user) {
    throw new Error('User not authenticated');
  }
  
  return await user.getIdToken();
};

// Helper to get headers with auth token
const getAuthHeaders = async () => {
  const token = await getAuthToken();
  return {
    'Authorization': `Bearer ${token}`
  };
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
    return response.data;
  } catch (error) {
    console.error('Error fetching active picks:', error);
    throw error;
  }
};

export const checkUserPicks = async (gameId) => {
  try {
    const headers = await getAuthHeaders();
    const response = await axios.post(`${API_BASE_URL}/picks/check`, { game_id: gameId }, { headers });
    return response.data;
  } catch (error) {
    console.error('Error checking user picks:', error);
    throw error;
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
    throw error;
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