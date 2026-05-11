import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Table, Button, Tag, Drawer, Descriptions, Select, message, Typography } from 'antd';
import { EyeOutlined, DownloadOutlined } from '@ant-design/icons';
import { formsAPI } from '@/api';
import type { FormSubmission } from '@/types';

const { Title } = Typography;

export default function FormSubmissions() {
  const { siteId } = useParams<{ siteId: string }>();
  const [submissions, setSubmissions] = useState<FormSubmission[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedSubmission, setSelectedSubmission] = useState<FormSubmission | null>(null);
  const [drawerVisible, setDrawerVisible] = useState(false);

  useEffect(() => {
    if (siteId) {
      loadSubmissions();
    }
  }, [siteId]);

  const loadSubmissions = async () => {
    setLoading(true);
    try {
      // Assuming we have a default form, in real app we'd load all forms first
      const response = await formsAPI.listSubmissions(siteId!, 'default-form-id');
      setSubmissions(response.items);
    } catch (error) {
      message.error('Failed to load submissions');
    } finally {
      setLoading(false);
    }
  };

  const handleView = (submission: FormSubmission) => {
    setSelectedSubmission(submission);
    setDrawerVisible(true);
  };

  const handleStatusChange = async (submissionId: string, status: string) => {
    try {
      await formsAPI.updateSubmissionStatus(siteId!, submissionId, { status: status as any });
      message.success('Status updated');
      loadSubmissions();
    } catch (error) {
      message.error('Failed to update status');
    }
  };

  const handleExport = async () => {
    try {
      const blob = await formsAPI.exportSubmissions(siteId!, 'default-form-id');
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'submissions.csv';
      a.click();
      message.success('Export started');
    } catch (error) {
      message.error('Failed to export');
    }
  };

  const columns = [
    {
      title: 'Submitted',
      dataIndex: 'submitted_at',
      key: 'submitted_at',
      render: (date: string) => new Date(date).toLocaleString(),
    },
    {
      title: 'Name',
      key: 'name',
      render: (_: any, record: FormSubmission) => record.data.name || '-',
    },
    {
      title: 'Email',
      key: 'email',
      render: (_: any, record: FormSubmission) => record.data.email || '-',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string, record: FormSubmission) => (
        <Select
          value={status}
          onChange={(value) => handleStatusChange(record.id, value)}
          size="small"
          style={{ width: 100 }}
        >
          <Select.Option value="new">
            <Tag color="blue">New</Tag>
          </Select.Option>
          <Select.Option value="read">
            <Tag color="orange">Read</Tag>
          </Select.Option>
          <Select.Option value="replied">
            <Tag color="green">Replied</Tag>
          </Select.Option>
          <Select.Option value="archived">
            <Tag color="gray">Archived</Tag>
          </Select.Option>
        </Select>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: FormSubmission) => (
        <Button size="small" icon={<EyeOutlined />} onClick={() => handleView(record)}>
          View
        </Button>
      ),
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <Title level={2}>Form Submissions</Title>
        <Button icon={<DownloadOutlined />} onClick={handleExport}>
          Export CSV
        </Button>
      </div>

      <Table columns={columns} dataSource={submissions} loading={loading} rowKey="id" />

      <Drawer
        title="Submission Details"
        open={drawerVisible}
        onClose={() => setDrawerVisible(false)}
        width={600}
      >
        {selectedSubmission && (
          <Descriptions column={1} bordered>
            <Descriptions.Item label="Submitted">
              {new Date(selectedSubmission.submitted_at).toLocaleString()}
            </Descriptions.Item>
            <Descriptions.Item label="IP Address">{selectedSubmission.ip_address}</Descriptions.Item>
            <Descriptions.Item label="Status">{selectedSubmission.status}</Descriptions.Item>
            {Object.entries(selectedSubmission.data).map(([key, value]) => (
              <Descriptions.Item label={key} key={key}>
                {String(value)}
              </Descriptions.Item>
            ))}
          </Descriptions>
        )}
      </Drawer>
    </div>
  );
}
