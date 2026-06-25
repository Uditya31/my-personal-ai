import create from 'zustand'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export const useConversationStore = create((set, get) => ({
  conversations: [],
  currentConversation: null,
  isLoading: false,
  error: null,

  createConversation: async (title, accessToken) => {
    set({ isLoading: true, error: null })
    try {
      const response = await axios.post(
        `${API_URL}/conversations/`,
        { title, description: '' },
        { headers: { Authorization: `Bearer ${accessToken}` } }
      )
      set((state) => ({
        conversations: [response.data, ...state.conversations],
        currentConversation: response.data,
        isLoading: false,
      }))
      return response.data
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Failed to create conversation', isLoading: false })
      throw error
    }
  },

  getConversations: async (accessToken) => {
    set({ isLoading: true, error: null })
    try {
      const response = await axios.get(`${API_URL}/conversations/`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      set({ conversations: response.data, isLoading: false })
      return response.data
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Failed to get conversations', isLoading: false })
      throw error
    }
  },

  getConversation: async (id, accessToken) => {
    set({ isLoading: true, error: null })
    try {
      const response = await axios.get(`${API_URL}/conversations/${id}`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      set({ currentConversation: response.data, isLoading: false })
      return response.data
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Failed to get conversation', isLoading: false })
      throw error
    }
  },

  updateConversation: async (id, data, accessToken) => {
    try {
      const response = await axios.put(`${API_URL}/conversations/${id}`, data, {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      set((state) => ({
        conversations: state.conversations.map((c) => (c.id === id ? response.data : c)),
        currentConversation: response.data,
      }))
      return response.data
    } catch (error) {
      throw error
    }
  },

  deleteConversation: async (id, accessToken) => {
    try {
      await axios.delete(`${API_URL}/conversations/${id}`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      set((state) => ({
        conversations: state.conversations.filter((c) => c.id !== id),
        currentConversation: state.currentConversation?.id === id ? null : state.currentConversation,
      }))
    } catch (error) {
      throw error
    }
  },

  searchConversations: async (query, accessToken) => {
    try {
      const response = await axios.get(`${API_URL}/conversations/search/${query}`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      set({ conversations: response.data })
      return response.data
    } catch (error) {
      throw error
    }
  },
}))
