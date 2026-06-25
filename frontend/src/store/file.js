import create from 'zustand'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export const useFileStore = create((set) => ({
  files: [],
  isLoading: false,
  error: null,

  uploadFile: async (file, accessToken) => {
    set({ isLoading: true, error: null })
    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await axios.post(`${API_URL}/files/upload`, formData, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'multipart/form-data',
        },
      })
      set((state) => ({
        files: [response.data, ...state.files],
        isLoading: false,
      }))
      return response.data
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Failed to upload file', isLoading: false })
      throw error
    }
  },

  getFiles: async (accessToken) => {
    set({ isLoading: true, error: null })
    try {
      const response = await axios.get(`${API_URL}/files/`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      set({ files: response.data, isLoading: false })
      return response.data
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Failed to get files', isLoading: false })
      throw error
    }
  },

  deleteFile: async (fileId, accessToken) => {
    try {
      await axios.delete(`${API_URL}/files/${fileId}`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      })
      set((state) => ({
        files: state.files.filter((f) => f.id !== fileId),
      }))
    } catch (error) {
      throw error
    }
  },
}))
