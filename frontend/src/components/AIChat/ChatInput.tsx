import { useState } from 'react';
import { Input, Button, Upload } from 'antd';
import { SendOutlined, PaperClipOutlined } from '@ant-design/icons';

const { TextArea } = Input;

interface ChatInputProps {
  onSend: (message: string) => void;
  onUpload?: (file: File) => void;
  disabled?: boolean;
  placeholder?: string;
}

export default function ChatInput({ onSend, onUpload, disabled, placeholder }: ChatInputProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (inputValue.trim()) {
      onSend(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleUpload = (file: File) => {
    if (onUpload) {
      onUpload(file);
    }
    return false;
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <div className="flex gap-2">
        <TextArea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder || 'Type your message... (Shift+Enter for new line)'}
          autoSize={{ minRows: 1, maxRows: 4 }}
          disabled={disabled}
          className="flex-1"
        />
        {onUpload && (
          <Upload
            beforeUpload={handleUpload}
            showUploadList={false}
            accept=".pdf,.doc,.docx,.txt"
          >
            <Button icon={<PaperClipOutlined />} disabled={disabled} />
          </Upload>
        )}
        <Button
          type="primary"
          icon={<SendOutlined />}
          onClick={handleSend}
          disabled={disabled || !inputValue.trim()}
        >
          Send
        </Button>
      </div>
    </div>
  );
}
