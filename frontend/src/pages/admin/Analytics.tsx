import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Row, Col, Statistic, Table, Typography, message } from 'antd';
import { EyeOutlined, UserOutlined, ArrowUpOutlined } from '@ant-design/icons';
import { analyticsAPI } from '@/api';
import type { AnalyticsOverview } from '@/types';

const { Title } = Typography;

export default function Analytics() {
  const { siteId } = useParams<{ siteId: string }>();
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (siteId) {
      loadAnalytics();
    }
  }, [siteId]);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const data = await analyticsAPI.getOverview(siteId!);
      setOverview(data);
    } catch (error) {
      message.error('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  const pageColumns = [
    {
      title: 'Page',
      dataIndex: 'page_path',
      key: 'page_path',
    },
    {
      title: 'Page Views',
      dataIndex: 'pv',
      key: 'pv',
    },
    {
      title: 'Unique Visitors',
      dataIndex: 'uv',
      key: 'uv',
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <Title level={2} className="mb-6">
        Analytics
      </Title>

      <Row gutter={[16, 16]} className="mb-6">
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="Total Page Views"
              value={overview?.total_pv || 0}
              prefix={<EyeOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="Unique Visitors"
              value={overview?.total_uv || 0}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="Form Submissions"
              value={overview?.form_submissions || 0}
              prefix={<ArrowUpOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Card title="Top Pages" loading={loading}>
        <Table
          columns={pageColumns}
          dataSource={[
            { page_path: '/', pv: 1250, uv: 850 },
            { page_path: '/about', pv: 456, uv: 320 },
            { page_path: '/contact', pv: 234, uv: 180 },
          ]}
          pagination={false}
          rowKey="page_path"
        />
      </Card>
    </div>
  );
}
