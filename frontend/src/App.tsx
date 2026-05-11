import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import './App.css';

// Layouts
import AppLayout from './components/Layout/AppLayout';
import ProtectedRoute from './components/common/ProtectedRoute';

// Auth Pages
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';

// Main Pages
import Dashboard from './pages/dashboard/Dashboard';
import AIBuilder from './pages/ai-builder/AIBuilder';
import Editor from './pages/editor/Editor';

// Admin Pages
import SiteSettings from './pages/admin/SiteSettings';
import BlogManager from './pages/admin/BlogManager';
import FormSubmissions from './pages/admin/FormSubmissions';
import Analytics from './pages/admin/Analytics';
import TeamManager from './pages/admin/TeamManager';

// Publish
import PublishPage from './pages/publish/PublishPage';

function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#3b82f6',
          borderRadius: 8,
        },
      }}
    >
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Routes */}
          <Route element={<ProtectedRoute />}>
            {/* Routes without layout (full-screen) */}
            <Route path="/ai-builder" element={<AIBuilder />} />
            <Route path="/ai-builder/:sessionId" element={<AIBuilder />} />
            <Route path="/sites/:siteId/editor" element={<Editor />} />

            {/* Routes with layout */}
            <Route element={<AppLayout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/sites/:siteId/settings" element={<SiteSettings />} />
              <Route path="/sites/:siteId/blog" element={<BlogManager />} />
              <Route path="/sites/:siteId/forms" element={<FormSubmissions />} />
              <Route path="/sites/:siteId/analytics" element={<Analytics />} />
              <Route path="/sites/:siteId/publish" element={<PublishPage />} />
              <Route path="/team" element={<TeamManager />} />
            </Route>
          </Route>

          {/* Catch all - redirect to dashboard or login */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </ConfigProvider>
  );
}

export default App;
