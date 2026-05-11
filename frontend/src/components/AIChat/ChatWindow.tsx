import { useEffect, useRef } from 'react';
import { Spin, Empty } from 'antd';
import ChatMessage from './ChatMessage';
import type { ChatMessage as ChatMessageType } from '@/types';

interface ChatWindowProps {
  messages: ChatMessageType[];
  loading?: boolean;
}

export default function ChatWindow({ messages, loading }: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 && !loading ? (
        <div className="h-full flex items-center justify-center">
          <Empty
            description="Start a conversation with AI to build your website"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        </div>
      ) : (
        <>
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          {loading && (
            <div className="flex items-center gap-3">
              <Spin size="small" />
              <span className="text-gray-500">AI is thinking...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  );
}
