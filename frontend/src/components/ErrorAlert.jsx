import { AlertCircle } from 'lucide-react'

const ErrorAlert = ({ message, onClose }) => (
  <div className="fixed top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded flex items-center gap-2 animate-slideIn">
    <AlertCircle className="w-5 h-5" />
    <span>{message}</span>
    {onClose && (
      <button onClick={onClose} className="ml-4 font-bold text-xl">
        ×
      </button>
    )}
  </div>
)

export default ErrorAlert
