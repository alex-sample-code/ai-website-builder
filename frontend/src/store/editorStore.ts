import { create } from 'zustand';
import type { Page } from '@/types';

interface EditorState {
  editor: any | null;
  currentPage: Page | null;
  isDirty: boolean;
  isSaving: boolean;
  lastSaved: Date | null;

  setEditor: (editor: any) => void;
  setCurrentPage: (page: Page | null) => void;
  setDirty: (isDirty: boolean) => void;
  setSaving: (isSaving: boolean) => void;
  setLastSaved: (date: Date) => void;
  reset: () => void;
}

export const useEditorStore = create<EditorState>((set) => ({
  editor: null,
  currentPage: null,
  isDirty: false,
  isSaving: false,
  lastSaved: null,

  setEditor: (editor: any) => {
    set({ editor });
  },

  setCurrentPage: (page: Page | null) => {
    set({ currentPage: page, isDirty: false });
  },

  setDirty: (isDirty: boolean) => {
    set({ isDirty });
  },

  setSaving: (isSaving: boolean) => {
    set({ isSaving });
  },

  setLastSaved: (date: Date) => {
    set({ lastSaved: date, isDirty: false });
  },

  reset: () => {
    set({
      editor: null,
      currentPage: null,
      isDirty: false,
      isSaving: false,
      lastSaved: null,
    });
  },
}));
