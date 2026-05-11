import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button, Select, Space, message, Spin } from 'antd';
import {
  SaveOutlined,
  EyeOutlined,
  CloudUploadOutlined,
  LeftOutlined,
  PlusOutlined,
} from '@ant-design/icons';
import GrapesEditor from '@/components/Editor/GrapesEditor';
import { useSiteStore, useEditorStore } from '@/store';
import { pagesAPI } from '@/api';
import type { Editor } from 'grapesjs';
import debounce from 'lodash/debounce';

export default function EditorPage() {
  const { siteId } = useParams<{ siteId: string }>();
  const navigate = useNavigate();
  const { pages, fetchPages } = useSiteStore();
  const { setEditor, setCurrentPage, setDirty, setSaving, setLastSaved } = useEditorStore();

  const [selectedPageId, setSelectedPageId] = useState<string>('');
  const [currentPageData, setCurrentPageData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (siteId) {
      loadPages();
    }
  }, [siteId]);

  useEffect(() => {
    if (pages.length > 0 && !selectedPageId) {
      const homepage = pages.find((p) => p.is_homepage) || pages[0];
      setSelectedPageId(homepage.id);
      loadPage(homepage.id);
    }
  }, [pages]);

  const loadPages = async () => {
    try {
      await fetchPages(siteId!);
    } catch (error) {
      message.error('Failed to load pages');
    }
  };

  const loadPage = async (pageId: string) => {
    if (!siteId) return;

    setLoading(true);
    try {
      const page = await pagesAPI.get(siteId, pageId);
      setCurrentPageData(page.grapesjs_data || {});
      setCurrentPage(page);
      setLoading(false);
    } catch (error) {
      message.error('Failed to load page');
      setLoading(false);
    }
  };

  const handleEditorInit = (editor: Editor) => {
    setEditor(editor);

    // Add custom blocks
    addCustomBlocks(editor);
  };

  const addCustomBlocks = (editor: Editor) => {
    const blockManager = editor.BlockManager;

    // Hero Block
    blockManager.add('hero-section', {
      label: 'Hero Banner',
      category: 'Sections',
      content: `
        <section class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20 px-4">
          <div class="max-w-4xl mx-auto text-center">
            <h1 class="text-5xl font-bold mb-6">Your Company Name</h1>
            <p class="text-xl mb-8">A brief description of what your company does</p>
            <a href="#contact" class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 inline-block">Get Started</a>
          </div>
        </section>
      `,
    });

    // Features Block
    blockManager.add('features-grid', {
      label: 'Features Grid',
      category: 'Sections',
      content: `
        <section class="py-16 px-4 bg-white">
          <div class="max-w-6xl mx-auto">
            <h2 class="text-4xl font-bold text-center mb-12">Our Features</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div class="text-center p-6">
                <div class="text-4xl mb-4">🚀</div>
                <h3 class="text-xl font-semibold mb-2">Fast</h3>
                <p class="text-gray-600">Lightning-fast performance</p>
              </div>
              <div class="text-center p-6">
                <div class="text-4xl mb-4">🎨</div>
                <h3 class="text-xl font-semibold mb-2">Beautiful</h3>
                <p class="text-gray-600">Stunning designs</p>
              </div>
              <div class="text-center p-6">
                <div class="text-4xl mb-4">🔒</div>
                <h3 class="text-xl font-semibold mb-2">Secure</h3>
                <p class="text-gray-600">Enterprise-grade security</p>
              </div>
            </div>
          </div>
        </section>
      `,
    });

    // Contact Form Block
    blockManager.add('contact-form', {
      label: 'Contact Form',
      category: 'Forms',
      content: `
        <section class="py-16 px-4 bg-gray-50">
          <div class="max-w-2xl mx-auto">
            <h2 class="text-4xl font-bold text-center mb-12">Contact Us</h2>
            <form class="space-y-4">
              <input type="text" placeholder="Name" class="w-full p-3 border border-gray-300 rounded-lg" />
              <input type="email" placeholder="Email" class="w-full p-3 border border-gray-300 rounded-lg" />
              <textarea placeholder="Message" rows="4" class="w-full p-3 border border-gray-300 rounded-lg"></textarea>
              <button type="submit" class="w-full bg-blue-600 text-white p-3 rounded-lg font-semibold hover:bg-blue-700">Send Message</button>
            </form>
          </div>
        </section>
      `,
    });
  };

  const debouncedSave = useCallback(
    debounce(async (editor: Editor) => {
      if (!siteId || !selectedPageId) return;

      setIsSaving(true);
      setSaving(true);

      try {
        const html = editor.getHtml();
        const css = editor.getCss();
        const grapesjs_data = editor.getProjectData();

        await pagesAPI.update(siteId, selectedPageId, {
          html,
          css,
          grapesjs_data,
        });

        setLastSaved(new Date());
        message.success('Page saved');
      } catch (error) {
        message.error('Failed to save page');
      } finally {
        setIsSaving(false);
        setSaving(false);
      }
    }, 2000),
    [siteId, selectedPageId]
  );

  const handleEditorChange = (editor: Editor) => {
    setDirty(true);
    debouncedSave(editor);
  };

  const handlePageChange = (pageId: string) => {
    setSelectedPageId(pageId);
    loadPage(pageId);
  };

  const handlePreview = () => {
    message.info('Preview feature coming soon');
  };

  const handlePublish = () => {
    navigate(`/sites/${siteId}/publish`);
  };

  const handleBack = () => {
    navigate('/');
  };

  if (loading && !currentPageData) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Spin size="large" tip="Loading editor..." />
      </div>
    );
  }

  return (
    <div className="fixed inset-0 flex flex-col bg-white">
      {/* Top Toolbar */}
      <div className="h-16 border-b border-gray-200 flex items-center justify-between px-4 bg-white">
        <Space>
          <Button icon={<LeftOutlined />} onClick={handleBack}>
            Back
          </Button>
          <Select
            value={selectedPageId}
            onChange={handlePageChange}
            style={{ width: 200 }}
            options={pages.map((page) => ({
              value: page.id,
              label: page.title + (page.is_homepage ? ' (Home)' : ''),
            }))}
          />
          <Button icon={<PlusOutlined />} disabled>
            New Page
          </Button>
        </Space>

        <Space>
          {isSaving && <Spin size="small" />}
          <Button icon={<SaveOutlined />} loading={isSaving}>
            {isSaving ? 'Saving...' : 'Saved'}
          </Button>
          <Button icon={<EyeOutlined />} onClick={handlePreview}>
            Preview
          </Button>
          <Button type="primary" icon={<CloudUploadOutlined />} onClick={handlePublish}>
            Publish
          </Button>
        </Space>
      </div>

      {/* Editor Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Blocks */}
        <div className="w-64 border-r border-gray-200 overflow-y-auto bg-white">
          <div className="p-4">
            <h3 className="font-semibold mb-4">Blocks</h3>
            <div id="blocks-container"></div>
          </div>
        </div>

        {/* Center - Canvas */}
        <div className="flex-1 overflow-hidden">
          <GrapesEditor
            onInit={handleEditorInit}
            onChange={handleEditorChange}
            initialData={currentPageData}
          />
        </div>

        {/* Right Panel - Styles & Layers */}
        <div className="w-80 border-l border-gray-200 overflow-y-auto bg-white">
          <div className="p-4">
            <h3 className="font-semibold mb-4">Styles</h3>
            <div id="styles-container"></div>
            <div id="traits-container" className="mt-4"></div>
            <h3 className="font-semibold mb-4 mt-8">Layers</h3>
            <div id="layers-container"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
