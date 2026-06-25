import { Plus, Menu, LogOut, Settings, Trash2 } from 'lucide-react'
import { useState } from 'react'

const Sidebar = ({
  conversations,
  currentConversationId,
  onSelectConversation,
  onCreateConversation,
  onDeleteConversation,
  onLogout,
}) => {
  const [isOpen, setIsOpen] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  const filteredConversations = conversations.filter((conv) =>
    conv.title.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div
      className={`${
        isOpen ? 'w-64' : 'w-20'
      } bg-gray-100 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col transition-all duration-300 h-screen`}
    >
      <div className="p-4 border-b border-gray-200 dark:border-gray-800">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-2 hover:bg-gray-200 dark:hover:bg-gray-800 rounded"
        >
          <Menu className="w-5 h-5" />
        </button>
        {isOpen && <h1 className="text-xl font-bold mt-2">My Personal AI</h1>}
      </div>

      <button
        onClick={onCreateConversation}
        className="m-4 p-2 bg-primary text-white rounded hover:bg-opacity-90 flex items-center gap-2"
      >
        <Plus className="w-5 h-5" />
        {isOpen && 'New Chat'}
      </button>

      {isOpen && (
        <div className="px-4 mb-4">
          <input
            type="text"
            placeholder="Search chats..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full p-2 border border-gray-300 dark:border-gray-700 rounded bg-white dark:bg-gray-800 text-sm"
          />
        </div>
      )}

      <div className="flex-1 overflow-y-auto scrollbar-hide">
        {filteredConversations.map((conv) => (
          <div
            key={conv.id}
            onClick={() => onSelectConversation(conv.id)}
            className={`p-3 cursor-pointer border-l-4 ${
              currentConversationId === conv.id
                ? 'border-primary bg-white dark:bg-gray-800'
                : 'border-transparent hover:bg-gray-200 dark:hover:bg-gray-800'
            }`}
          >
            {isOpen && (
              <>
                <p className="font-semibold truncate">{conv.title}</p>
                <p className="text-xs text-gray-500 truncate">New Chat</p>
              </>
            )}
            {!isOpen && <div className="w-3 h-3 bg-primary rounded-full" />}
          </div>
        ))}
      </div>

      <div className="border-t border-gray-200 dark:border-gray-800 p-4 space-y-2">
        <button className="w-full p-2 hover:bg-gray-200 dark:hover:bg-gray-800 rounded flex items-center gap-2">
          <Settings className="w-5 h-5" />
          {isOpen && 'Settings'}
        </button>
        <button
          onClick={onLogout}
          className="w-full p-2 hover:bg-red-100 dark:hover:bg-red-900 rounded flex items-center gap-2 text-red-600"
        >
          <LogOut className="w-5 h-5" />
          {isOpen && 'Logout'}
        </button>
      </div>
    </div>
  )
}

export default Sidebar
