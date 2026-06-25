import { useState } from 'react'
import { Send, Plus, Paperclip } from 'lucide-react'

const ChatInput = ({ onSendMessage, onFileUpload, isLoading }) => {
  const [message, setMessage] = useState('')
  const [files, setFiles] = useState([])

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message)
      setMessage('')
      setFiles([])
    }
  }

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files)
    setFiles(selectedFiles)
    selectedFiles.forEach(file => {
      onFileUpload(file)
    })
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
      <div className="flex items-end gap-3">
        <div className="flex-1">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 dark:text-white resize-none focus:outline-none focus:ring-2 focus:ring-primary"
            rows="3"
          />
        </div>
        <div className="flex gap-2">
          <label className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
            <Paperclip className="w-5 h-5" />
            <input
              type="file"
              multiple
              onChange={handleFileChange}
              className="hidden"
              accept=".pdf,.docx,.txt"
            />
          </label>
          <button
            onClick={handleSend}
            disabled={!message.trim() || isLoading}
            className="p-2 bg-primary text-white rounded hover:bg-opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
      {files.length > 0 && (
        <div className="mt-2 flex gap-2 flex-wrap">
          {files.map((file, index) => (
            <span key={index} className="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
              {file.name}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

export default ChatInput
