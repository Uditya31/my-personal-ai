import create from 'zustand'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export const useMessageStore = create((set, get) => ({
  messages: [],
  isLoading: false,
  error: null,

  getMessages: async (conversationId, accessToken) => {
    set({ isLoading: true, error: null })
    try {
      const response = await axios.get(`${API_URL}/messages/conversation/${conversationId}`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      set({ messages: response.data, isLoading: false })
      return response.data
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Failed to get messages', isLoading: false })
      throw error
    }
  },

  sendMessage: async (conversationId, content, accessToken) => {
    try {
      const response = await axios.post(
        `${API_URL}/messages/conversation/${conversationId}/send`,
        { content },
        { headers: { Authorization: `Bearer ${accessToken}` } }
      )
      set((state) => ({
        messages: [...state.messages, response.data],
      }))
      return response.data
    } catch (error) {
      throw error
    }
  },

  streamMessage: async (conversationId, content, accessToken, onChunk) => {
    try {
      const response = await axios.post(
        `${API_URL}/messages/conversation/${conversationId}/stream`,
        { content },
        {
          headers: { Authorization: `Bearer ${accessToken}` },
          responseType: 'stream',
        }
      )
      return response
    } catch (error) {
      throw error
    }
  },

  deleteMessage: async (messageId, accessToken) => {
    try {
      await axios.delete(`${API_URL}/messages/message/${messageId}`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      set((state) => ({
        messages: state.messages.filter((m) => m.id !== messageId),
      }))
    } catch (error) {
      throw error
    }
  },

  clearMessages: () => set({ messages: [] }),
}))
