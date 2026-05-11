import { Outlet } from 'react-router-dom';
import { Layout } from 'antd';
import Sidebar from './Sidebar';
import Header from './Header';

const { Sider, Content } = Layout;

export default function AppLayout() {
  return (
    <Layout className="min-h-screen">
      <Sider width={240} className="fixed left-0 top-0 bottom-0 overflow-auto">
        <Sidebar />
      </Sider>
      <Layout className="ml-60">
        <Header />
        <Content className="p-6 bg-gray-50">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
