import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Table, Button, Modal, Form, Input, message, Space, Tag, Typography } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { blogAPI } from '@/api';
import type { BlogPost } from '@/types';

const { Title } = Typography;
const { TextArea } = Input;

export default function BlogManager() {
  const { siteId } = useParams<{ siteId: string }>();
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingPost, setEditingPost] = useState<BlogPost | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    if (siteId) {
      loadPosts();
    }
  }, [siteId]);

  const loadPosts = async () => {
    setLoading(true);
    try {
      const response = await blogAPI.listPosts(siteId!);
      setPosts(response.items);
    } catch (error) {
      message.error('Failed to load blog posts');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setEditingPost(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (post: BlogPost) => {
    setEditingPost(post);
    form.setFieldsValue(post);
    setModalVisible(true);
  };

  const handleDelete = async (postId: string) => {
    try {
      await blogAPI.deletePost(siteId!, postId);
      message.success('Post deleted');
      loadPosts();
    } catch (error) {
      message.error('Failed to delete post');
    }
  };

  const handleSave = async (values: any) => {
    try {
      if (editingPost) {
        await blogAPI.updatePost(siteId!, editingPost.id, values);
        message.success('Post updated');
      } else {
        await blogAPI.createPost(siteId!, {
          ...values,
          slug: values.title.toLowerCase().replace(/\s+/g, '-'),
        });
        message.success('Post created');
      }
      setModalVisible(false);
      loadPosts();
    } catch (error) {
      message.error('Failed to save post');
    }
  };

  const columns = [
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'published' ? 'green' : 'orange'}>{status}</Tag>
      ),
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: BlogPost) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => handleEdit(record)} />
          <Button
            size="small"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
          />
        </Space>
      ),
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <Title level={2}>Blog Posts</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
          New Post
        </Button>
      </div>

      <Table columns={columns} dataSource={posts} loading={loading} rowKey="id" />

      <Modal
        title={editingPost ? 'Edit Post' : 'New Post'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleSave}>
          <Form.Item name="title" label="Title" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="excerpt" label="Excerpt">
            <Input />
          </Form.Item>
          <Form.Item name="content" label="Content" rules={[{ required: true }]}>
            <TextArea rows={6} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
