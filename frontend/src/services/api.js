import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const newsAPI = {
  async getNews(limit = 10) {
    const response = await api.get(`/api/news?limit=${limit}`);
    return response.data;
  },

  async refreshNews(limit = 10) {
    // Force refresh by using force_refresh parameter
    const response = await api.get(`/api/news?limit=${limit}&force_refresh=true`);
    return response.data;
  },

  async getHealth() {
    const response = await api.get('/health');
    return response.data;
  }
};

export default api;

