import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Card, Button, Typography, message, Progress, Space } from 'antd';
import { CheckOutlined, RobotOutlined, ReloadOutlined } from '@ant-design/icons';
import ChatWindow from '@/components/AIChat/ChatWindow';
import ChatInput from '@/components/AIChat/ChatInput';
import { aiAPI } from '@/api';
import type { AISession, ChatMessage } from '@/types';

const { Title, Text } = Typography;

export default function AIBuilder() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const siteId = searchParams.get('siteId');

  const [session, setSession] = useState<AISession | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [previewHtml, setPreviewHtml] = useState<string>('');
  const [generationProgress, setGenerationProgress] = useState(0);

  useEffect(() => {
    initSession();
  }, [siteId]);

  const initSession = async () => {
    try {
      const newSession = await aiAPI.createSession({ site_name: 'New Site' });
      setSession(newSession);

      // Add initial AI message
      const initialMessage: ChatMessage = {
        role: 'assistant',
        content:
          "Hi! I'm your AI website builder. I'll help you create an amazing website. Let's start with a few questions:\n\n1. What's your company name?\n2. What industry are you in?\n3. What's the main purpose of your website?\n\nYou can also upload a company document (PDF, Word, or TXT) to help me understand your business better.",
        timestamp: new Date().toISOString(),
      };
      setMessages([initialMessage]);
    } catch (error) {
      message.error('Failed to initialize AI session');
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!session) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const updatedSession = await aiAPI.sendMessage(session.id, { message: content });

      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: updatedSession.conversation[updatedSession.conversation.length - 1]?.content || 'Received',
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, aiMessage]);
      setSession(updatedSession);

      // Check if we have enough info to generate
      if (updatedSession.generated_config && !generating) {
        promptGeneration();
      }
    } catch (error) {
      message.error('Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  const handleUploadDocument = async (file: File) => {
    if (!session) return;

    try {
      message.loading('Uploading document...', 0);
      await aiAPI.uploadDocument(session.id, file);
      message.destroy();
      message.success('Document uploaded successfully!');

      const aiMessage: ChatMessage = {
        role: 'assistant',
        content:
          "Great! I've received your document. Let me analyze it... Based on this, I can create a professional website for you. Would you like me to generate the website now?",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      message.destroy();
      message.error('Failed to upload document');
    }
  };

  const promptGeneration = () => {
    const aiMessage: ChatMessage = {
      role: 'assistant',
      content:
        "Perfect! I have enough information now. I can generate your website with:\n\n- Homepage with hero section\n- About Us page\n- Products/Services page\n- Contact page\n- Blog section\n\nShall I proceed with the generation?",
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, aiMessage]);
  };

  const handleGenerate = async () => {
    if (!session) return;

    setGenerating(true);
    setGenerationProgress(0);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setGenerationProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 500);

      await aiAPI.generate(session.id);

      clearInterval(progressInterval);
      setGenerationProgress(100);

      message.success('Website generated successfully!');

      // Mock preview HTML (in real app, this would come from the backend)
      const mockHtml = `
        <!DOCTYPE html>
        <html>
          <head>
            <style>
              body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
              .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 100px 20px; text-center; }
              h1 { font-size: 48px; margin-bottom: 20px; }
              p { font-size: 20px; opacity: 0.9; }
            </style>
          </head>
          <body>
            <div class="hero">
              <h1>Welcome to Your Website</h1>
              <p>AI-generated professional website</p>
            </div>
          </body>
        </html>
      `;
      setPreviewHtml(mockHtml);

      const aiMessage: ChatMessage = {
        role: 'assistant',
        content:
          "✨ Your website is ready! Check the preview on the right. You can:\n\n- Click 'Looks Great!' to go to the editor for fine-tuning\n- Click 'Regenerate' to create a different version\n- Or tell me what you'd like to change",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      message.error('Failed to generate website');
    } finally {
      setGenerating(false);
    }
  };

  const handleConfirm = () => {
    if (siteId) {
      navigate(`/sites/${siteId}/editor`);
    } else {
      message.info('Creating site and redirecting to editor...');
      // In real implementation, save the generated site and redirect
    }
  };

  return (
    <div className="fixed inset-0 flex bg-gray-50">
      {/* Left Panel - Chat */}
      <div className="w-1/2 flex flex-col border-r border-gray-200 bg-white">
        <div className="border-b border-gray-200 p-4 bg-gradient-to-r from-purple-600 to-blue-600">
          <Space>
            <RobotOutlined className="text-2xl text-white" />
            <Title level={4} className="m-0 text-white">
              AI Website Builder
            </Title>
          </Space>
        </div>

        <ChatWindow messages={messages} loading={loading} />

        {generating && (
          <div className="p-4 border-t border-gray-200 bg-blue-50">
            <Text strong className="block mb-2">
              Generating your website...
            </Text>
            <Progress percent={generationProgress} status="active" />
          </div>
        )}

        {messages.length > 2 && !generating && !previewHtml && (
          <div className="p-4 border-t border-gray-200 bg-green-50">
            <Button
              type="primary"
              size="large"
              block
              icon={<RobotOutlined />}
              onClick={handleGenerate}
            >
              Generate Website Now
            </Button>
          </div>
        )}

        <ChatInput
          onSend={handleSendMessage}
          onUpload={handleUploadDocument}
          disabled={loading || generating}
        />
      </div>

      {/* Right Panel - Preview */}
      <div className="w-1/2 flex flex-col bg-gray-100">
        <div className="border-b border-gray-200 p-4 bg-white flex items-center justify-between">
          <Title level={4} className="m-0">
            Live Preview
          </Title>
          {previewHtml && (
            <Space>
              <Button icon={<ReloadOutlined />} onClick={handleGenerate}>
                Regenerate
              </Button>
              <Button type="primary" icon={<CheckOutlined />} onClick={handleConfirm}>
                Looks Great!
              </Button>
            </Space>
          )}
        </div>

        <div className="flex-1 overflow-auto p-4">
          {previewHtml ? (
            <Card className="h-full">
              <iframe
                srcDoc={previewHtml}
                className="w-full h-full border-0"
                title="Website Preview"
                sandbox="allow-same-origin"
              />
            </Card>
          ) : (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <RobotOutlined className="text-6xl text-gray-300 mb-4" />
                <Title level={4} type="secondary">
                  Your website preview will appear here
                </Title>
                <Text type="secondary">Answer a few questions to get started</Text>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
