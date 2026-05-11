import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Card,
  Button,
  Table,
  Modal,
  Input,
  Typography,
  Space,
  Tag,
  Steps,
  Alert,
  message,
} from 'antd';
import {
  CloudUploadOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  GlobalOutlined,
  RollbackOutlined,
} from '@ant-design/icons';
import { publishAPI } from '@/api';
import type { SiteVersion, DomainStatus } from '@/types';

const { Title, Text, Paragraph } = Typography;

export default function PublishPage() {
  const { siteId } = useParams<{ siteId: string }>();
  const [versions, setVersions] = useState<SiteVersion[]>([]);
  const [domainStatus, setDomainStatus] = useState<DomainStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [publishing, setPublishing] = useState(false);
  const [domainModalVisible, setDomainModalVisible] = useState(false);
  const [customDomain, setCustomDomain] = useState('');

  useEffect(() => {
    if (siteId) {
      loadVersions();
      loadDomainStatus();
    }
  }, [siteId]);

  const loadVersions = async () => {
    try {
      const data = await publishAPI.listVersions(siteId!);
      setVersions(data);
    } catch (error) {
      message.error('Failed to load versions');
    }
  };

  const loadDomainStatus = async () => {
    try {
      const data = await publishAPI.getDomainStatus(siteId!);
      setDomainStatus(data);
    } catch (error) {
      console.error('No domain configured');
    }
  };

  const handlePublish = async () => {
    setPublishing(true);
    try {
      await publishAPI.publish(siteId!, { notes: 'Manual publish' });
      message.success('Site published successfully!');
      loadVersions();
    } catch (error) {
      message.error('Failed to publish site');
    } finally {
      setPublishing(false);
    }
  };

  const handleRollback = async (versionId: string) => {
    Modal.confirm({
      title: 'Rollback to this version?',
      content: 'This will replace your current published site with this version.',
      onOk: async () => {
        try {
          await publishAPI.rollback(siteId!, versionId);
          message.success('Rolled back successfully');
          loadVersions();
        } catch (error) {
          message.error('Failed to rollback');
        }
      },
    });
  };

  const handleBindDomain = async () => {
    if (!customDomain.trim()) {
      message.error('Please enter a domain');
      return;
    }

    setLoading(true);
    try {
      const data = await publishAPI.bindDomain(siteId!, { custom_domain: customDomain.trim() });
      setDomainStatus(data);
      setDomainModalVisible(false);
      message.success('Domain binding initiated');
    } catch (error) {
      message.error('Failed to bind domain');
    } finally {
      setLoading(false);
    }
  };

  const getDomainStatusStep = () => {
    if (!domainStatus?.custom_domain) return 0;
    switch (domainStatus.domain_status) {
      case 'pending':
        return 0;
      case 'dns_configured':
        return 1;
      case 'ssl_provisioning':
        return 2;
      case 'active':
        return 3;
      default:
        return 0;
    }
  };

  const versionColumns = [
    {
      title: 'Version',
      dataIndex: 'version_number',
      key: 'version_number',
      render: (version: number, record: SiteVersion) => (
        <Space>
          <Text strong>v{version}</Text>
          {record.is_current && <Tag color="green">Current</Tag>}
        </Space>
      ),
    },
    {
      title: 'Published',
      dataIndex: 'published_at',
      key: 'published_at',
      render: (date: string) => new Date(date).toLocaleString(),
    },
    {
      title: 'Notes',
      dataIndex: 'notes',
      key: 'notes',
      render: (notes: string) => notes || '-',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: SiteVersion) =>
        !record.is_current && (
          <Button
            size="small"
            icon={<RollbackOutlined />}
            onClick={() => handleRollback(record.id)}
          >
            Rollback
          </Button>
        ),
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <Title level={2} className="mb-6">
        Publish & Domain
      </Title>

      {/* Publish Section */}
      <Card className="mb-6">
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <div>
            <Title level={4}>Ready to Publish?</Title>
            <Paragraph type="secondary">
              Publishing will make your website live and accessible to visitors.
            </Paragraph>
          </div>

          <Button
            type="primary"
            size="large"
            icon={<CloudUploadOutlined />}
            onClick={handlePublish}
            loading={publishing}
          >
            {publishing ? 'Publishing...' : 'Publish Now'}
          </Button>
        </Space>
      </Card>

      {/* Domain Management */}
      <Card title="Custom Domain" className="mb-6">
        {domainStatus?.custom_domain ? (
          <Space direction="vertical" style={{ width: '100%' }} size="large">
            <Alert
              message={`Domain: ${domainStatus.custom_domain}`}
              type={domainStatus.domain_status === 'active' ? 'success' : 'info'}
              icon={
                domainStatus.domain_status === 'active' ? (
                  <CheckCircleOutlined />
                ) : (
                  <ClockCircleOutlined />
                )
              }
            />

            <Steps
              current={getDomainStatusStep()}
              items={[
                {
                  title: 'Domain Added',
                  description: 'Configure DNS',
                },
                {
                  title: 'DNS Verified',
                  description: 'Provisioning SSL',
                },
                {
                  title: 'SSL Ready',
                  description: 'Activating',
                },
                {
                  title: 'Active',
                  description: 'Site Live',
                },
              ]}
            />

            {domainStatus.cname_target && (
              <Alert
                message="DNS Configuration Required"
                description={
                  <div>
                    <Paragraph>Add the following CNAME record to your DNS:</Paragraph>
                    <Text code copyable>
                      {domainStatus.cname_target}
                    </Text>
                  </div>
                }
                type="warning"
              />
            )}
          </Space>
        ) : (
          <Space direction="vertical" style={{ width: '100%' }}>
            <Paragraph>
              Connect your custom domain to make your site accessible at your own URL.
            </Paragraph>
            <Button
              type="primary"
              icon={<GlobalOutlined />}
              onClick={() => setDomainModalVisible(true)}
            >
              Connect Domain
            </Button>
          </Space>
        )}
      </Card>

      {/* Version History */}
      <Card title="Version History">
        <Table columns={versionColumns} dataSource={versions} rowKey="id" />
      </Card>

      {/* Domain Modal */}
      <Modal
        title="Connect Custom Domain"
        open={domainModalVisible}
        onCancel={() => setDomainModalVisible(false)}
        onOk={handleBindDomain}
        confirmLoading={loading}
      >
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <div>
            <Text strong>Enter your domain name</Text>
            <Input
              placeholder="www.yourcompany.com"
              value={customDomain}
              onChange={(e) => setCustomDomain(e.target.value)}
              prefix={<GlobalOutlined />}
              size="large"
              className="mt-2"
            />
          </div>
          <Alert
            message="Make sure you have access to your domain's DNS settings"
            type="info"
            showIcon
          />
        </Space>
      </Modal>
    </div>
  );
}
