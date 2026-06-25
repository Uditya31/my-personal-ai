import { useEffect, useRef } from 'react'
import { Trash2 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

const ChatMessage = ({ message, onDelete }) => {
  const isUser = message.role === 'user'
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [message])

  return (
    <div className={`flex gap-4 message-animation ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`flex-1 max-w-md p-3 rounded-lg ${
          isUser
            ? 'bg-primary text-white rounded-br-none'
            : 'bg-gray-200 dark:bg-gray-700 dark:text-white rounded-bl-none'
        }`}
      >
        <div className="prose dark:prose-invert max-w-none text-sm">
          <ReactMarkdown
            components={{
              code({ inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '')
                return !inline && match ? (
                  <SyntaxHighlighter
                    style={oneDark}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                )
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
        <div className="flex items-center justify-between mt-2 gap-2">
          <span className="text-xs opacity-70">{new Date(message.created_at).toLocaleTimeString()}</span>
          {isUser && (
            <button
              onClick={() => onDelete(message.id)}
              className="hover:opacity-70"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
      <div ref={messagesEndRef} />
    </div>
  )
}

export default ChatMessage
