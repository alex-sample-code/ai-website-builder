import { useEffect, useRef } from 'react';
import grapesjs from 'grapesjs';
import 'grapesjs/dist/css/grapes.min.css';
import gjsPresetWebpage from 'grapesjs-preset-webpage';
import gjsBlocksBasic from 'grapesjs-blocks-basic';
import type { Editor } from 'grapesjs';

interface GrapesEditorProps {
  onInit?: (editor: Editor) => void;
  onChange?: (editor: Editor) => void;
  initialData?: any;
}

export default function GrapesEditor({ onInit, onChange, initialData }: GrapesEditorProps) {
  const editorRef = useRef<HTMLDivElement>(null);
  const editorInstance = useRef<Editor | null>(null);

  useEffect(() => {
    if (!editorRef.current) return;

    const editor = grapesjs.init({
      container: editorRef.current,
      height: '100%',
      width: 'auto',
      storageManager: false,
      plugins: [gjsPresetWebpage, gjsBlocksBasic],
      pluginsOpts: {
        'gjs-preset-webpage': {
          blocks: ['column1', 'column2', 'column3', 'text', 'link', 'image', 'video'],
        },
        'gjs-blocks-basic': {},
      },
      canvas: {
        styles: [
          'https://cdn.jsdelivr.net/npm/tailwindcss@3.4.0/dist/tailwind.min.css',
        ],
      },
      deviceManager: {
        devices: [
          {
            id: 'desktop',
            name: 'Desktop',
            width: '',
          },
          {
            id: 'tablet',
            name: 'Tablet',
            width: '768px',
          },
          {
            id: 'mobile',
            name: 'Mobile',
            width: '375px',
          },
        ],
      },
      layerManager: {
        appendTo: '#layers-container',
      },
      styleManager: {
        appendTo: '#styles-container',
        sectors: [
          {
            name: 'General',
            open: true,
            properties: [
              {
                name: 'Display',
                property: 'display',
              },
              {
                name: 'Width',
                property: 'width',
              },
              {
                name: 'Height',
                property: 'height',
              },
            ],
          },
          {
            name: 'Typography',
            open: false,
            properties: [
              {
                name: 'Font Family',
                property: 'font-family',
              },
              {
                name: 'Font Size',
                property: 'font-size',
              },
              {
                name: 'Font Weight',
                property: 'font-weight',
              },
              {
                name: 'Color',
                property: 'color',
              },
              {
                name: 'Text Align',
                property: 'text-align',
              },
            ],
          },
          {
            name: 'Decorations',
            open: false,
            properties: [
              {
                name: 'Background',
                property: 'background-color',
              },
              {
                name: 'Border',
                property: 'border',
              },
              {
                name: 'Border Radius',
                property: 'border-radius',
              },
            ],
          },
          {
            name: 'Extra',
            open: false,
            properties: [
              {
                name: 'Margin',
                property: 'margin',
              },
              {
                name: 'Padding',
                property: 'padding',
              },
            ],
          },
        ],
      },
      blockManager: {
        appendTo: '#blocks-container',
      },
      traitManager: {
        appendTo: '#traits-container',
      },
    });

    // Load initial data
    if (initialData) {
      editor.loadProjectData(initialData);
    }

    // Listen for changes
    editor.on('change:changesCount', () => {
      if (onChange) {
        onChange(editor);
      }
    });

    editorInstance.current = editor;

    if (onInit) {
      onInit(editor);
    }

    return () => {
      editor.destroy();
    };
  }, []);

  return <div ref={editorRef} className="gjs-editor" />;
}
