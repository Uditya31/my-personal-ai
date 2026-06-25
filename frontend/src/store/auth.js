import create from 'zustand'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export const useAuthStore = create((set) => ({
  user: null,
  accessToken: localStorage.getItem('accessToken'),
  refreshToken: localStorage.getItem('refreshToken'),
  isLoading: false,
  error: null,

  login: async (email, password) => {
    set({ isLoading: true, error: null })
    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        email,
        password,
      })
      const { access_token, refresh_token } = response.data
      localStorage.setItem('accessToken', access_token)
      localStorage.setItem('refreshToken', refresh_token)
      set({
        accessToken: access_token,
        refreshToken: refresh_token,
        isLoading: false,
      })
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Login failed'
      set({ error: errorMessage, isLoading: false })
      throw error
    }
  },

  register: async (username, email, password, fullName) => {
    set({ isLoading: true, error: null })
    try {
      const response = await axios.post(`${API_URL}/auth/register`, {
        username,
        email,
        password,
        full_name: fullName,
      })
      set({ isLoading: false })
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Registration failed'
      set({ error: errorMessage, isLoading: false })
      throw error
    }
  },

  logout: () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    set({ user: null, accessToken: null, refreshToken: null })
  },

  getCurrentUser: async (accessToken) => {
    try {
      const response = await axios.get(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      set({ user: response.data })
      return response.data
    } catch (error) {
      console.error('Failed to get current user:', error)
    }
  },
}))
