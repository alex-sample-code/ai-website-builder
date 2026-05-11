import { create } from 'zustand';
import type { Site, Page } from '@/types';
import { sitesAPI, pagesAPI } from '@/api';

interface SiteState {
  sites: Site[];
  currentSite: Site | null;
  pages: Page[];
  isLoading: boolean;
  error: string | null;

  fetchSites: () => Promise<void>;
  createSite: (name: string, templateId?: string) => Promise<Site>;
  setCurrentSite: (site: Site | null) => void;
  fetchPages: (siteId: string) => Promise<void>;
  createPage: (siteId: string, title: string, slug: string, isHomepage?: boolean) => Promise<Page>;
  updatePage: (siteId: string, pageId: string, data: Partial<Page>) => Promise<void>;
  deletePage: (siteId: string, pageId: string) => Promise<void>;
  clearError: () => void;
}

export const useSiteStore = create<SiteState>((set) => ({
  sites: [],
  currentSite: null,
  pages: [],
  isLoading: false,
  error: null,

  fetchSites: async () => {
    set({ isLoading: true, error: null });
    try {
      const sites = await sitesAPI.list();
      set({ sites, isLoading: false });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to fetch sites';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  createSite: async (name: string, templateId?: string) => {
    set({ isLoading: true, error: null });
    try {
      const site = await sitesAPI.create({ name, template_id: templateId });
      set((state) => ({
        sites: [...state.sites, site],
        currentSite: site,
        isLoading: false,
      }));
      return site;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to create site';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  setCurrentSite: (site: Site | null) => {
    set({ currentSite: site });
  },

  fetchPages: async (siteId: string) => {
    set({ isLoading: true, error: null });
    try {
      const pages = await pagesAPI.list(siteId);
      set({ pages, isLoading: false });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to fetch pages';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  createPage: async (siteId: string, title: string, slug: string, isHomepage?: boolean) => {
    set({ isLoading: true, error: null });
    try {
      const page = await pagesAPI.create(siteId, {
        title,
        slug,
        is_homepage: isHomepage,
      });
      set((state) => ({
        pages: [...state.pages, page],
        isLoading: false,
      }));
      return page;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to create page';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  updatePage: async (siteId: string, pageId: string, data: Partial<Page>) => {
    set({ isLoading: true, error: null });
    try {
      const updatedPage = await pagesAPI.update(siteId, pageId, data);
      set((state) => ({
        pages: state.pages.map((p) => (p.id === pageId ? updatedPage : p)),
        isLoading: false,
      }));
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to update page';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  deletePage: async (siteId: string, pageId: string) => {
    set({ isLoading: true, error: null });
    try {
      await pagesAPI.delete(siteId, pageId);
      set((state) => ({
        pages: state.pages.filter((p) => p.id !== pageId),
        isLoading: false,
      }));
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to delete page';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  clearError: () => {
    set({ error: null });
  },
}));
