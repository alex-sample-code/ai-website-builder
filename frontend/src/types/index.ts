// User & Auth Types
export interface User {
  id: string;
  tenant_id: string;
  email: string;
  name: string;
  role: 'owner' | 'editor' | 'viewer';
  avatar_url?: string;
  last_login_at?: string;
  created_at: string;
}

export interface Tenant {
  id: string;
  name: string;
  plan: 'free' | 'pro' | 'enterprise';
  custom_domain?: string;
  cf_tenant_id?: string;
  domain_status?: 'pending' | 'dns_configured' | 'ssl_provisioning' | 'active' | 'error';
  status: 'active' | 'suspended' | 'deleted';
  ai_quota_used: number;
  ai_quota_limit: number;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  company_name: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type?: string;
  expires_in?: number;
  user?: User;
  tenant?: Tenant;
}

// Site Types
export interface Site {
  id: string;
  tenant_id: string;
  name: string;
  status: 'draft' | 'published' | 'offline';
  template_id?: string;
  current_version_id?: string;
  published_at?: string;
  publish_url?: string;
  settings_snapshot?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface SiteCreateRequest {
  name: string;
  template_id?: string;
}

// Page Types
export interface Page {
  id: string;
  site_id: string;
  slug: string;
  title: string;
  seo_meta?: SEOMeta;
  grapesjs_data?: any;
  html?: string;
  css?: string;
  js?: string;
  is_homepage: boolean;
  sort_order: number;
  status: 'active' | 'hidden' | 'deleted';
  created_at: string;
  updated_at: string;
}

export interface SEOMeta {
  title?: string;
  description?: string;
  og_image?: string;
  og_title?: string;
  keywords?: string[];
}

export interface PageCreateRequest {
  slug: string;
  title: string;
  seo_meta?: SEOMeta;
  is_homepage?: boolean;
}

export interface PageUpdateRequest {
  title?: string;
  slug?: string;
  seo_meta?: SEOMeta;
  grapesjs_data?: any;
  html?: string;
  css?: string;
  js?: string;
}

// AI Builder Types
export interface AISession {
  id: string;
  tenant_id: string;
  site_id?: string;
  conversation: ChatMessage[];
  company_info?: string;
  company_info_s3_key?: string;
  generated_config?: any;
  generated_pages?: any[];
  model_id: string;
  input_tokens: number;
  output_tokens: number;
  generation_time_ms: number;
  status: 'in_progress' | 'completed' | 'failed';
  created_at: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface AISessionCreateRequest {
  site_name?: string;
}

export interface AIMessageRequest {
  message: string;
}

export interface AIGenerateRequest {
  force_regenerate?: boolean;
}

// Site Settings Types
export interface SiteSettings {
  id: string;
  site_id: string;
  logo_url?: string;
  favicon_url?: string;
  company_name?: string;
  company_address?: string;
  company_phone?: string;
  company_email?: string;
  social_links?: SocialLinks;
  analytics_id?: string;
  custom_head_code?: string;
  custom_body_code?: string;
  color_scheme?: ColorScheme;
  font_family?: string;
  updated_at: string;
}

export interface SocialLinks {
  wechat?: string;
  weibo?: string;
  linkedin?: string;
  twitter?: string;
  facebook?: string;
  instagram?: string;
}

export interface ColorScheme {
  primary?: string;
  secondary?: string;
  accent?: string;
  background?: string;
  text?: string;
}

export interface NavMenu {
  id: string;
  site_id: string;
  position: 'header' | 'footer' | 'sidebar';
  items: NavMenuItem[];
  updated_at: string;
}

export interface NavMenuItem {
  label: string;
  url: string;
  target?: '_blank' | '_self';
  children?: NavMenuItem[];
}

// Blog Types
export interface BlogPost {
  id: string;
  site_id: string;
  category_id?: string;
  title: string;
  slug: string;
  content: string;
  content_html?: string;
  excerpt?: string;
  cover_image?: string;
  seo_title?: string;
  seo_description?: string;
  author_name?: string;
  status: 'draft' | 'published' | 'archived';
  published_at?: string;
  scheduled_at?: string;
  created_at: string;
  updated_at: string;
}

export interface BlogCategory {
  id: string;
  site_id: string;
  name: string;
  slug: string;
  sort_order: number;
}

export interface BlogTag {
  id: string;
  site_id: string;
  name: string;
  slug: string;
}

export interface BlogPostCreateRequest {
  title: string;
  slug: string;
  content: string;
  excerpt?: string;
  cover_image?: string;
  category_id?: string;
  tags?: string[];
  status?: 'draft' | 'published';
  scheduled_at?: string;
}

// Form Types
export interface FormDefinition {
  id: string;
  site_id: string;
  name: string;
  fields: FormField[];
  notification_emails: string[];
  webhook_url?: string;
  success_message?: string;
  is_enabled: boolean;
  created_at: string;
}

export interface FormField {
  name: string;
  type: 'text' | 'email' | 'tel' | 'textarea' | 'select' | 'checkbox' | 'radio';
  label: string;
  required: boolean;
  placeholder?: string;
  options?: string[];
}

export interface FormSubmission {
  id: string;
  site_id: string;
  form_def_id: string;
  page_id?: string;
  data: Record<string, any>;
  status: 'new' | 'read' | 'replied' | 'archived';
  replied_at?: string;
  notes?: string;
  ip_address?: string;
  user_agent?: string;
  submitted_at: string;
}

export interface FormSubmissionUpdateRequest {
  status?: 'new' | 'read' | 'replied' | 'archived';
  notes?: string;
}

// Analytics Types
export interface AnalyticsOverview {
  total_pv: number;
  total_uv: number;
  pv_trend: TrendData[];
  uv_trend: TrendData[];
  form_submissions: number;
  avg_session_duration?: number;
}

export interface TrendData {
  date: string;
  value: number;
}

export interface PageAnalytics {
  page_path: string;
  pv: number;
  uv: number;
  avg_time?: number;
}

export interface SourceAnalytics {
  source: string;
  visits: number;
  percentage: number;
}

export interface DeviceAnalytics {
  device_type: 'desktop' | 'mobile' | 'tablet';
  visits: number;
  percentage: number;
}

// Asset Types
export interface Asset {
  id: string;
  tenant_id: string;
  site_id?: string;
  filename: string;
  s3_key: string;
  cdn_url: string;
  content_type: string;
  size_bytes: number;
  width?: number;
  height?: number;
  folder?: string;
  created_at: string;
}

export interface AssetUploadResponse {
  upload_url: string;
  asset_id: string;
  cdn_url: string;
}

// Team Types
export interface TeamMember {
  id: string;
  tenant_id: string;
  email: string;
  name: string;
  role: 'owner' | 'editor' | 'viewer';
  avatar_url?: string;
  last_login_at?: string;
  created_at: string;
}

export interface TeamInvitation {
  id: string;
  tenant_id: string;
  email: string;
  role: 'owner' | 'editor' | 'viewer';
  token: string;
  status: 'pending' | 'accepted' | 'expired';
  invited_by: string;
  created_at: string;
  expires_at: string;
}

export interface TeamInviteRequest {
  email: string;
  role: 'editor' | 'viewer';
}

// Publish Types
export interface SiteVersion {
  id: string;
  site_id: string;
  version_number: number;
  snapshot: any;
  s3_prefix: string;
  published_by: string;
  published_at: string;
  is_current: boolean;
  notes?: string;
}

export interface PublishRequest {
  notes?: string;
}

export interface DomainBindRequest {
  custom_domain: string;
}

export interface DomainStatus {
  custom_domain?: string;
  domain_status: 'pending' | 'dns_configured' | 'ssl_provisioning' | 'active' | 'error';
  cname_target?: string;
  dns_verified: boolean;
  ssl_status?: string;
}

// Template Types
export interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  thumbnail_url: string;
  preview_url: string;
  is_premium: boolean;
  created_at: string;
}

// Audit Log Types
export interface AuditLog {
  id: string;
  tenant_id: string;
  user_id: string;
  action: string;
  resource_type: string;
  resource_id: string;
  details: Record<string, any>;
  ip_address: string;
  created_at: string;
}

// API Response Types
export interface APIResponse<T = any> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface APIError {
  detail: string;
  code?: string;
}
