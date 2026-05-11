import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Form, Input, Button, message, Card, Typography } from 'antd';
import { MailOutlined, LockOutlined, TeamOutlined } from '@ant-design/icons';
import { useAuthStore } from '@/store';

const { Title, Text } = Typography;

export default function Register() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const register = useAuthStore((state) => state.register);

  const onFinish = async (values: { email: string; password: string; company_name: string }) => {
    setLoading(true);
    try {
      await register(values.email, values.password, values.company_name);
      message.success('Registration successful!');
      navigate('/');
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <Card className="w-full max-w-md shadow-lg">
        <div className="text-center mb-8">
          <Title level={2} className="mb-2">
            Create Your Account
          </Title>
          <Text type="secondary">Start building amazing websites with AI</Text>
        </div>

        <Form
          name="register"
          onFinish={onFinish}
          layout="vertical"
          size="large"
          autoComplete="off"
        >
          <Form.Item
            name="company_name"
            label="Company Name"
            rules={[{ required: true, message: 'Please enter your company name' }]}
          >
            <Input
              prefix={<TeamOutlined />}
              placeholder="Your Company"
              autoComplete="organization"
            />
          </Form.Item>

          <Form.Item
            name="email"
            label="Email Address"
            rules={[
              { required: true, message: 'Please enter your email' },
              { type: 'email', message: 'Please enter a valid email' },
            ]}
          >
            <Input
              prefix={<MailOutlined />}
              placeholder="you@company.com"
              autoComplete="email"
            />
          </Form.Item>

          <Form.Item
            name="password"
            label="Password"
            rules={[
              { required: true, message: 'Please enter your password' },
              { min: 8, message: 'Password must be at least 8 characters' },
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="At least 8 characters"
              autoComplete="new-password"
            />
          </Form.Item>

          <Form.Item
            name="confirm_password"
            label="Confirm Password"
            dependencies={['password']}
            rules={[
              { required: true, message: 'Please confirm your password' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('Passwords do not match'));
                },
              }),
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Confirm password"
              autoComplete="new-password"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              className="h-12"
            >
              Create Account
            </Button>
          </Form.Item>

          <div className="text-center">
            <Text type="secondary">
              Already have an account?{' '}
              <Link to="/login" className="text-blue-600 hover:text-blue-700">
                Sign in
              </Link>
            </Text>
          </div>
        </Form>
      </Card>
    </div>
  );
}
