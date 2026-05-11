import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Form, Input, Upload, Button, message, Typography } from 'antd';
import { UploadOutlined, SaveOutlined } from '@ant-design/icons';
import { settingsAPI } from '@/api';

const { Title } = Typography;
const { TextArea } = Input;

export default function SiteSettings() {
  const { siteId } = useParams<{ siteId: string }>();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (siteId) {
      loadSettings();
    }
  }, [siteId]);

  const loadSettings = async () => {
    try {
      const data = await settingsAPI.get(siteId!);
      form.setFieldsValue(data);
    } catch (error) {
      message.error('Failed to load settings');
    }
  };

  const handleSave = async (values: any) => {
    setLoading(true);
    try {
      await settingsAPI.update(siteId!, values);
      message.success('Settings saved successfully');
    } catch (error) {
      message.error('Failed to save settings');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <Title level={2} className="mb-6">
        Site Settings
      </Title>

      <Form form={form} layout="vertical" onFinish={handleSave}>
        <Card title="Company Information" className="mb-4">
          <Form.Item name="company_name" label="Company Name">
            <Input placeholder="Your Company Name" />
          </Form.Item>

          <Form.Item name="company_email" label="Contact Email">
            <Input type="email" placeholder="contact@company.com" />
          </Form.Item>

          <Form.Item name="company_phone" label="Phone Number">
            <Input placeholder="+1 (555) 123-4567" />
          </Form.Item>

          <Form.Item name="company_address" label="Address">
            <TextArea rows={3} placeholder="123 Main St, City, State, ZIP" />
          </Form.Item>
        </Card>

        <Card title="Branding" className="mb-4">
          <Form.Item name="logo_url" label="Logo">
            <Upload>
              <Button icon={<UploadOutlined />}>Upload Logo</Button>
            </Upload>
          </Form.Item>

          <Form.Item name="favicon_url" label="Favicon">
            <Upload>
              <Button icon={<UploadOutlined />}>Upload Favicon</Button>
            </Upload>
          </Form.Item>
        </Card>

        <Card title="SEO & Analytics" className="mb-4">
          <Form.Item name="analytics_id" label="Google Analytics ID">
            <Input placeholder="G-XXXXXXXXXX" />
          </Form.Item>

          <Form.Item name="custom_head_code" label="Custom Head Code">
            <TextArea rows={4} placeholder="<script>...</script>" />
          </Form.Item>
        </Card>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} icon={<SaveOutlined />}>
            Save Settings
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
