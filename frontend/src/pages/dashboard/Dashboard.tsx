import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Modal, Input, Select, Row, Col, Empty, Typography, Space, Badge, message } from 'antd';
import { PlusOutlined, RobotOutlined, FileTextOutlined, EyeOutlined, SettingOutlined } from '@ant-design/icons';
import { useSiteStore, useAuthStore } from '@/store';
import Loading from '@/components/common/Loading';
import type { Site } from '@/types';

const { Title, Text } = Typography;

export default function Dashboard() {
  const navigate = useNavigate();
  const { sites, isLoading, fetchSites, createSite } = useSiteStore();
  const { tenant } = useAuthStore();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [createLoading, setCreateLoading] = useState(false);
  const [siteName, setSiteName] = useState('');
  const [buildMode, setBuildMode] = useState<'ai' | 'blank'>('ai');

  useEffect(() => {
    fetchSites();
  }, [fetchSites]);

  const handleCreateSite = async () => {
    if (!siteName.trim()) {
      message.error('Please enter a site name');
      return;
    }

    setCreateLoading(true);
    try {
      const site = await createSite(siteName.trim());

      if (buildMode === 'ai') {
        navigate(`/ai-builder?siteId=${site.id}`);
      } else {
        navigate(`/sites/${site.id}/editor`);
      }

      setIsModalOpen(false);
      setSiteName('');
    } catch (error) {
      message.error('Failed to create site');
    } finally {
      setCreateLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const statusMap: Record<string, { color: string; text: string }> = {
      draft: { color: 'default', text: 'Draft' },
      published: { color: 'success', text: 'Published' },
      offline: { color: 'error', text: 'Offline' },
    };
    const config = statusMap[status] || statusMap.draft;
    return <Badge status={config.color as any} text={config.text} />;
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <Title level={2} className="mb-2">
            My Websites
          </Title>
          <Text type="secondary">Manage and build your websites with AI</Text>
        </div>
        <Button
          type="primary"
          size="large"
          icon={<PlusOutlined />}
          onClick={() => setIsModalOpen(true)}
        >
          Create New Site
        </Button>
      </div>

      {/* Stats Cards */}
      <Row gutter={[16, 16]} className="mb-8">
        <Col xs={24} sm={8}>
          <Card>
            <div className="text-center">
              <Text type="secondary">Total Sites</Text>
              <div className="text-3xl font-bold text-blue-600 mt-2">{sites.length}</div>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <div className="text-center">
              <Text type="secondary">Published</Text>
              <div className="text-3xl font-bold text-green-600 mt-2">
                {sites.filter((s) => s.status === 'published').length}
              </div>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <div className="text-center">
              <Text type="secondary">AI Quota</Text>
              <div className="text-3xl font-bold text-purple-600 mt-2">
                {tenant?.ai_quota_used || 0} / {tenant?.ai_quota_limit || 0}
              </div>
            </div>
          </Card>
        </Col>
      </Row>

      {/* Site Cards */}
      {sites.length === 0 ? (
        <Card>
          <Empty
            image={Empty.PRESENTED_IMAGE_SIMPLE}
            description={
              <Space direction="vertical">
                <Text>No websites yet</Text>
                <Text type="secondary">Create your first website with AI</Text>
              </Space>
            }
          >
            <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>
              Create Your First Site
            </Button>
          </Empty>
        </Card>
      ) : (
        <Row gutter={[16, 16]}>
          {sites.map((site: Site) => (
            <Col xs={24} sm={12} lg={8} key={site.id}>
              <Card
                hoverable
                cover={
                  <div className="h-48 bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
                    <FileTextOutlined className="text-6xl text-gray-400" />
                  </div>
                }
                actions={[
                  <Button
                    type="text"
                    icon={<EyeOutlined />}
                    onClick={() => window.open(site.publish_url, '_blank')}
                    disabled={!site.publish_url}
                  >
                    Preview
                  </Button>,
                  <Button
                    type="text"
                    icon={<SettingOutlined />}
                    onClick={() => navigate(`/sites/${site.id}/settings`)}
                  >
                    Settings
                  </Button>,
                ]}
              >
                <Card.Meta
                  title={
                    <div className="flex items-center justify-between">
                      <span className="truncate">{site.name}</span>
                      {getStatusBadge(site.status)}
                    </div>
                  }
                  description={
                    <div className="mt-2">
                      <Text type="secondary" className="text-xs">
                        Updated: {new Date(site.updated_at).toLocaleDateString()}
                      </Text>
                    </div>
                  }
                />
                <div className="mt-4">
                  <Button
                    type="primary"
                    block
                    onClick={() => navigate(`/sites/${site.id}/editor`)}
                  >
                    Edit Site
                  </Button>
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      )}

      {/* Create Site Modal */}
      <Modal
        title="Create New Website"
        open={isModalOpen}
        onOk={handleCreateSite}
        onCancel={() => {
          setIsModalOpen(false);
          setSiteName('');
          setBuildMode('ai');
        }}
        confirmLoading={createLoading}
        okText="Create"
      >
        <Space direction="vertical" className="w-full" size="large">
          <div>
            <Text strong>Site Name</Text>
            <Input
              size="large"
              placeholder="My Awesome Website"
              value={siteName}
              onChange={(e) => setSiteName(e.target.value)}
              className="mt-2"
            />
          </div>

          <div>
            <Text strong>Build Mode</Text>
            <Select
              size="large"
              value={buildMode}
              onChange={setBuildMode}
              className="w-full mt-2"
              options={[
                {
                  value: 'ai',
                  label: (
                    <Space>
                      <RobotOutlined />
                      <span>AI Builder (Recommended)</span>
                    </Space>
                  ),
                },
                {
                  value: 'blank',
                  label: (
                    <Space>
                      <FileTextOutlined />
                      <span>Blank Template</span>
                    </Space>
                  ),
                },
              ]}
            />
            <Text type="secondary" className="text-xs mt-1 block">
              {buildMode === 'ai'
                ? 'Let AI generate your website through conversation'
                : 'Start with a blank template and build manually'}
            </Text>
          </div>
        </Space>
      </Modal>
    </div>
  );
}
