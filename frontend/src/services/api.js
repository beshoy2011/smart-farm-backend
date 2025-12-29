import axios from 'axios'
import { useAuthStore } from '../store/authStore'

// Use proxy in development, direct URL in production
const API_URL = import.meta.env.VITE_API_URL || (
  import.meta.env.DEV 
    ? '/api'  // Use Vite proxy in development
    : 'http://localhost:8000/api'  // Direct URL in production
)

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,  // Important for CORS with credentials
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    // Try to get token from store first, then from localStorage
    const token = useAuthStore.getState().token || localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

