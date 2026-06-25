import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/auth'
import { useEffect, useState } from 'react'

const ProtectedRoute = ({ children }) => {
  const { accessToken, getCurrentUser } = useAuthStore()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (accessToken) {
      getCurrentUser(accessToken).finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [accessToken, getCurrentUser])

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>
  }

  return accessToken ? children : <Navigate to="/login" />
}

export default ProtectedRoute
