import { create } from 'zustand'
import api from '../services/api'
import { setCurrentUserId } from '../modules/smartfarm/DataStore'

const useAuthStore = create((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true, // Add loading state

  login: async (username, password) => {
    try {
      const formData = new URLSearchParams()
      formData.append('username', username)
      formData.append('password', password)
      
      const response = await api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })
      const { access_token } = response.data
      set({ token: access_token, isAuthenticated: true })
      
      // Get user info
      const userResponse = await api.get('/auth/me', {
        headers: { Authorization: `Bearer ${access_token}` },
      })
      const newUser = userResponse.data
      
      // Don't clear old user data - keep it for when they log back in
      // Just switch to new user's data
      set({ user: newUser })
      
      // Store token and user ID in localStorage
      localStorage.setItem('auth_token', access_token)
      localStorage.setItem('current_user_id', newUser.id.toString())
      setCurrentUserId(newUser.id)
      
      return { success: true }
    } catch (error) {
      console.error('Login error:', error)
      let errorMessage = 'Login failed'
      if (error.response?.data) {
        if (error.response.data.detail) {
          errorMessage = typeof error.response.data.detail === 'string' 
            ? error.response.data.detail 
            : JSON.stringify(error.response.data.detail)
        } else if (error.response.data.message) {
          errorMessage = error.response.data.message
        }
      } else if (error.message) {
        errorMessage = error.message
      } else if (error.code === 'ERR_NETWORK') {
        errorMessage = 'Cannot connect to server. Please check if backend is running.'
      }
      return { success: false, error: errorMessage }
    }
  },

  register: async (userData) => {
    try {
      const response = await api.post('/auth/register', userData)
      const { access_token } = response.data
      set({ token: access_token, isAuthenticated: true })
      
      // Store token in localStorage
      localStorage.setItem('auth_token', access_token)
      
      // Get user info
      const userResponse = await api.get('/auth/me', {
        headers: { Authorization: `Bearer ${access_token}` },
      })
      const newUser = userResponse.data
      
      // Don't clear old user data - keep it for when they log back in
      // Just switch to new user's data
      set({ user: newUser })
      localStorage.setItem('current_user_id', newUser.id.toString())
      setCurrentUserId(newUser.id)
      
      return { success: true }
    } catch (error) {
      console.error('Registration error:', error)
      let errorMessage = 'Registration failed'
      if (error.response?.data) {
        if (error.response.data.detail) {
          errorMessage = typeof error.response.data.detail === 'string' 
            ? error.response.data.detail 
            : JSON.stringify(error.response.data.detail)
        } else if (error.response.data.message) {
          errorMessage = error.response.data.message
        } else if (Array.isArray(error.response.data)) {
          // Handle validation errors
          errorMessage = error.response.data.map(err => err.msg || err.message).join(', ')
        }
      } else if (error.message) {
        errorMessage = error.message
      } else if (error.code === 'ERR_NETWORK') {
        errorMessage = 'Cannot connect to server. Please check if backend is running.'
      }
      return { success: false, error: errorMessage }
    }
  },

  logout: () => {
    // Don't clear user data - keep it for when user logs back in
    localStorage.removeItem('auth_token')
    localStorage.removeItem('current_user_id')
    setCurrentUserId(null)
    
    // Just clear the cache in memory, but keep data in localStorage
    set({ user: null, token: null, isAuthenticated: false })
  },

  setUser: (user) => set({ user }),
  setToken: (token) => {
    localStorage.setItem('auth_token', token)
    set({ token, isAuthenticated: !!token })
  },

  loginWithGoogle: async (googleToken) => {
    try {
      const response = await api.post('/auth/google', { access_token: googleToken })
      const { access_token } = response.data
      set({ token: access_token, isAuthenticated: true })
      
      // Store token in localStorage
      localStorage.setItem('auth_token', access_token)
      
      // Get user info
      const userResponse = await api.get('/auth/me', {
        headers: { Authorization: `Bearer ${access_token}` },
      })
      const newUser = userResponse.data
      
      // Don't clear old user data - keep it for when they log back in
      // Just switch to new user's data
      set({ user: newUser })
      localStorage.setItem('current_user_id', newUser.id.toString())
      setCurrentUserId(newUser.id)
      
      return { success: true }
    } catch (error) {
      console.error('Google login error:', error)
      let errorMessage = 'Google login failed'
      if (error.response?.data) {
        if (error.response.data.detail) {
          errorMessage = typeof error.response.data.detail === 'string' 
            ? error.response.data.detail 
            : JSON.stringify(error.response.data.detail)
        } else if (error.response.data.message) {
          errorMessage = error.response.data.message
        }
      } else if (error.message) {
        errorMessage = error.message
      } else if (error.code === 'ERR_NETWORK') {
        errorMessage = 'Cannot connect to server. Please check if backend is running.'
      }
      return { success: false, error: errorMessage }
    }
  },

  init: () => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      set({ token, isAuthenticated: true, isLoading: true })
      // Fetch user info in background (non-blocking with timeout)
      const timeoutId = setTimeout(() => {
        set({ isLoading: false })
      }, 3000) // Max 3 seconds wait
      
      api.get('/auth/me', {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 3000 // 3 second timeout
      }).then(response => {
        clearTimeout(timeoutId)
        const user = response.data
        set({ user, isLoading: false })
        if (user?.id) {
          localStorage.setItem('current_user_id', user.id.toString())
          setCurrentUserId(user.id)
        }
      }).catch((error) => {
        clearTimeout(timeoutId)
        set({ isLoading: false })
        // Only clear token if it's a 401 (unauthorized)
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token')
          localStorage.removeItem('current_user_id')
          setCurrentUserId(null)
          set({ token: null, isAuthenticated: false })
        }
        // If backend is down, keep token for when it comes back
      })
    } else {
      set({ isLoading: false })
    }
  }
}))

// Initialize on load
if (typeof window !== 'undefined') {
  useAuthStore.getState().init()
}

export { useAuthStore }
export default useAuthStore
