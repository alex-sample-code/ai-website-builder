import { Link, useLocation, useParams } from 'react-router-dom';
import { Menu } from 'antd';
import {
  DashboardOutlined,
  RobotOutlined,
  EditOutlined,
  SettingOutlined,
  FileTextOutlined,
  FormOutlined,
  BarChartOutlined,
  TeamOutlined,
  CloudUploadOutlined,
} from '@ant-design/icons';

export default function Sidebar() {
  const location = useLocation();
  const { siteId } = useParams();

  const getSelectedKey = () => {
    if (location.pathname === '/') return 'dashboard';
    if (location.pathname.includes('/ai-builder')) return 'ai-builder';
    if (location.pathname.includes('/editor')) return 'editor';
    if (location.pathname.includes('/settings')) return 'settings';
    if (location.pathname.includes('/blog')) return 'blog';
    if (location.pathname.includes('/forms')) return 'forms';
    if (location.pathname.includes('/analytics')) return 'analytics';
    if (location.pathname.includes('/team')) return 'team';
    if (location.pathname.includes('/publish')) return 'publish';
    return 'dashboard';
  };

  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: <Link to="/">Dashboard</Link>,
    },
    ...(siteId
      ? [
          {
            key: 'editor',
            icon: <EditOutlined />,
            label: <Link to={`/sites/${siteId}/editor`}>Editor</Link>,
          },
          {
            key: 'settings',
            icon: <SettingOutlined />,
            label: <Link to={`/sites/${siteId}/settings`}>Settings</Link>,
          },
          {
            key: 'blog',
            icon: <FileTextOutlined />,
            label: <Link to={`/sites/${siteId}/blog`}>Blog</Link>,
          },
          {
            key: 'forms',
            icon: <FormOutlined />,
            label: <Link to={`/sites/${siteId}/forms`}>Forms</Link>,
          },
          {
            key: 'analytics',
            icon: <BarChartOutlined />,
            label: <Link to={`/sites/${siteId}/analytics`}>Analytics</Link>,
          },
          {
            key: 'publish',
            icon: <CloudUploadOutlined />,
            label: <Link to={`/sites/${siteId}/publish`}>Publish</Link>,
          },
        ]
      : []),
    {
      key: 'team',
      icon: <TeamOutlined />,
      label: <Link to="/team">Team</Link>,
    },
  ];

  return (
    <div className="h-full bg-gray-900">
      <div className="p-4 border-b border-gray-800">
        <Link to="/" className="flex items-center space-x-2">
          <RobotOutlined className="text-2xl text-blue-500" />
          <span className="text-white font-semibold text-lg">AI Builder</span>
        </Link>
      </div>
      <Menu
        mode="inline"
        selectedKeys={[getSelectedKey()]}
        items={menuItems}
        className="bg-gray-900 border-r-0"
        theme="dark"
      />
    </div>
  );
}
