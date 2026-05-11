import { Avatar, Dropdown, Button, Space, Typography } from 'antd';
import { UserOutlined, LogoutOutlined, DownOutlined } from '@ant-design/icons';
import { useAuthStore } from '@/store';
import { useNavigate } from 'react-router-dom';
import type { MenuProps } from 'antd';

const { Text } = Typography;

export default function Header() {
  const { user, tenant, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profile',
      onClick: () => {
        // Navigate to profile page
      },
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      danger: true,
      onClick: handleLogout,
    },
  ];

  return (
    <div className="h-16 bg-white border-b border-gray-200 px-6 flex items-center justify-between">
      <div>
        {tenant && (
          <Space>
            <Text strong className="text-lg">
              {tenant.name}
            </Text>
            <Text type="secondary" className="text-xs uppercase">
              {tenant.plan}
            </Text>
          </Space>
        )}
      </div>

      <Dropdown menu={{ items: menuItems }} trigger={['click']}>
        <Button type="text" className="h-10">
          <Space>
            <Avatar
              size="small"
              icon={<UserOutlined />}
              src={user?.avatar_url}
              className="bg-blue-500"
            />
            <Text>{user?.name || user?.email}</Text>
            <DownOutlined className="text-xs" />
          </Space>
        </Button>
      </Dropdown>
    </div>
  );
}
