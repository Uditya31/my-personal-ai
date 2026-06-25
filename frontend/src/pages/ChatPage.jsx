import { useEffect, useState } from 'react'
import { useAuthStore, useConversationStore, useMessageStore, useFileStore } from '../store'
import Sidebar from '../components/Sidebar'
import ChatMessage from '../components/ChatMessage'
import ChatInput from '../components/ChatInput'
import ErrorAlert from '../components/ErrorAlert'
import { useNavigate } from 'react-router-dom'

const ChatPage = () => {
  const navigate = useNavigate()
  const { accessToken, logout } = useAuthStore()
  const { conversations, currentConversation, createConversation, getConversations, getConversation, deleteConversation } = useConversationStore()
  const { messages, getMessages, sendMessage, deleteMessage } = useMessageStore()
  const { uploadFile } = useFileStore()
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    loadConversations()
  }, [accessToken])

  const loadConversations = async () => {
    try {
      const convs = await getConversations(accessToken)
      if (convs.length > 0) {
        await loadConversation(convs[0].id)
      }
    } catch (err) {
      setError('Failed to load conversations')
    }
  }

  const loadConversation = async (id) => {
    try {
      await getConversation(id, accessToken)
      await getMessages(id, accessToken)
    } catch (err) {
      setError('Failed to load conversation')
    }
  }

  const handleCreateConversation = async () => {
    try {
      const conv = await createConversation('New Chat', accessToken)
      await loadConversation(conv.id)
    } catch (err) {
      setError('Failed to create conversation')
    }
  }

  const handleSelectConversation = (id) => {
    loadConversation(id)
  }

  const handleDeleteConversation = async (id) => {
    try {
      await deleteConversation(id, accessToken)
      if (currentConversation?.id === id) {
        const remaining = conversations.filter(c => c.id !== id)
        if (remaining.length > 0) {
          await loadConversation(remaining[0].id)
        } else {
          await handleCreateConversation()
        }
      }
    } catch (err) {
      setError('Failed to delete conversation')
    }
  }

  const handleSendMessage = async (content) => {
    setIsLoading(true)
    try {
      await sendMessage(currentConversation.id, content, accessToken)
      await getMessages(currentConversation.id, accessToken)
    } catch (err) {
      setError('Failed to send message')
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileUpload = async (file) => {
    try {
      await uploadFile(file, accessToken)
    } catch (err) {
      setError('Failed to upload file')
    }
  }

  const handleDeleteMessage = async (id) => {
    try {
      await deleteMessage(id, accessToken)
      await getMessages(currentConversation.id, accessToken)
    } catch (err) {
      setError('Failed to delete message')
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex h-screen bg-white dark:bg-gray-950">
      {error && <ErrorAlert message={error} onClose={() => setError('')} />}
      <Sidebar
        conversations={conversations}
        currentConversationId={currentConversation?.id}
        onSelectConversation={handleSelectConversation}
        onCreateConversation={handleCreateConversation}
        onDeleteConversation={handleDeleteConversation}
        onLogout={handleLogout}
      />
      <div className="flex-1 flex flex-col">
        {currentConversation ? (
          <>
            <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-hide">
              {messages.length === 0 ? (
                <div className="h-full flex items-center justify-center text-gray-500">
                  <p>Start a conversation by typing a message below</p>
                </div>
              ) : (
                messages.map((msg) => (
                  <ChatMessage key={msg.id} message={msg} onDelete={handleDeleteMessage} />
                ))
              )}
            </div>
            <ChatInput onSendMessage={handleSendMessage} onFileUpload={handleFileUpload} isLoading={isLoading} />
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <button
              onClick={handleCreateConversation}
              className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-opacity-90"
            >
              Start New Conversation
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatPage
