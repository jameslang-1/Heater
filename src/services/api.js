// src/services/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const fetchGames = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/games`);
    return response.data;
  } catch (error) {
    console.error('Error fetching games:', error);
    throw error;
  }
};

export const fetchGameById = async (gameId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/games/${gameId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching game:', error);
    throw error;
  }
};

export const updateOdds = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/update-odds`);
    return response.data;
  } catch (error) {
    console.error('Error updating odds:', error);
    throw error;
  }
};