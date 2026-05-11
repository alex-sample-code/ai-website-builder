import { Avatar, Typography } from 'antd';
import { UserOutlined, RobotOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import type { ChatMessage as ChatMessageType } from '@/types';

const { Text } = Typography;

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <Avatar
        icon={isUser ? <UserOutlined /> : <RobotOutlined />}
        className={isUser ? 'bg-blue-500' : 'bg-purple-500'}
      />
      <div
        className={`flex-1 max-w-3xl ${
          isUser ? 'text-right' : 'text-left'
        }`}
      >
        <div
          className={`inline-block p-4 rounded-lg ${
            isUser
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 text-gray-900'
          }`}
        >
          {isUser ? (
            <Text className="text-white">{message.content}</Text>
          ) : (
            <div className="prose prose-sm max-w-none">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>
        <div className="mt-1">
          <Text type="secondary" className="text-xs">
            {new Date(message.timestamp).toLocaleTimeString()}
          </Text>
        </div>
      </div>
    </div>
  );
}
