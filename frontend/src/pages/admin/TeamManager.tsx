import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, Tag, message, Typography } from 'antd';
import { PlusOutlined, DeleteOutlined, MailOutlined } from '@ant-design/icons';
import { teamAPI } from '@/api';
import type { TeamMember } from '@/types';

const { Title } = Typography;

export default function TeamManager() {
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    loadMembers();
  }, []);

  const loadMembers = async () => {
    setLoading(true);
    try {
      const data = await teamAPI.listMembers();
      setMembers(data);
    } catch (error) {
      message.error('Failed to load team members');
    } finally {
      setLoading(false);
    }
  };

  const handleInvite = async (values: any) => {
    try {
      await teamAPI.invite(values);
      message.success('Invitation sent');
      setModalVisible(false);
      form.resetFields();
      loadMembers();
    } catch (error) {
      message.error('Failed to send invitation');
    }
  };

  const handleRemove = async (memberId: string) => {
    try {
      await teamAPI.removeMember(memberId);
      message.success('Member removed');
      loadMembers();
    } catch (error) {
      message.error('Failed to remove member');
    }
  };

  const handleRoleChange = async (memberId: string, role: string) => {
    try {
      await teamAPI.updateRole(memberId, role as any);
      message.success('Role updated');
      loadMembers();
    } catch (error) {
      message.error('Failed to update role');
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Role',
      dataIndex: 'role',
      key: 'role',
      render: (role: string, record: TeamMember) => (
        <Select
          value={role}
          onChange={(value) => handleRoleChange(record.id, value)}
          size="small"
          style={{ width: 120 }}
        >
          <Select.Option value="owner">
            <Tag color="red">Owner</Tag>
          </Select.Option>
          <Select.Option value="editor">
            <Tag color="blue">Editor</Tag>
          </Select.Option>
          <Select.Option value="viewer">
            <Tag color="green">Viewer</Tag>
          </Select.Option>
        </Select>
      ),
    },
    {
      title: 'Last Login',
      dataIndex: 'last_login_at',
      key: 'last_login_at',
      render: (date: string) => (date ? new Date(date).toLocaleString() : 'Never'),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: TeamMember) =>
        record.role !== 'owner' && (
          <Button
            size="small"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleRemove(record.id)}
          >
            Remove
          </Button>
        ),
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <Title level={2}>Team Management</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
          Invite Member
        </Button>
      </div>

      <Table columns={columns} dataSource={members} loading={loading} rowKey="id" />

      <Modal
        title="Invite Team Member"
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleInvite}>
          <Form.Item
            name="email"
            label="Email Address"
            rules={[
              { required: true, message: 'Please enter email' },
              { type: 'email', message: 'Please enter valid email' },
            ]}
          >
            <Input prefix={<MailOutlined />} placeholder="colleague@company.com" />
          </Form.Item>
          <Form.Item name="role" label="Role" initialValue="editor" rules={[{ required: true }]}>
            <Select>
              <Select.Option value="editor">Editor - Can edit content</Select.Option>
              <Select.Option value="viewer">Viewer - Read-only access</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
