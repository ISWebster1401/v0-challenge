import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const newsAPI = {
  async getNews(limit = 10, fromDate = null, toDate = null) {
    let url = `/api/news?limit=${limit}`;
    if (fromDate) {
      url += `&from_date=${fromDate}`;
    }
    if (toDate) {
      url += `&to_date=${toDate}`;
    }
    const response = await api.get(url);
    return response.data;
  },

  async refreshNews(limit = 10, fromDate = null, toDate = null) {
    // Force refresh by using force_refresh parameter
    let url = `/api/news?limit=${limit}&force_refresh=true`;
    if (fromDate) {
      url += `&from_date=${fromDate}`;
    }
    if (toDate) {
      url += `&to_date=${toDate}`;
    }
    const response = await api.get(url);
    return response.data;
  },

  async getFullSummary(url) {
    const response = await api.post('/api/summarize/full', { url });
    return response.data;
  },

  async getHealth() {
    const response = await api.get('/health');
    return response.data;
  }
};

export default api;

