import { Loader } from 'lucide-react'

const LoadingSpinner = () => (
  <div className="flex items-center justify-center h-screen">
    <div className="flex flex-col items-center gap-4">
      <Loader className="w-8 h-8 animate-spin text-primary" />
      <p className="text-gray-600 dark:text-gray-400">Loading...</p>
    </div>
  </div>
)

export default LoadingSpinner
